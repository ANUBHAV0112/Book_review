import time
import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app import crud, models, schemas
from .database import SessionLocal, engine, Base
import fakeredis


app = FastAPI(
    title="Book Review API",
    description="Manage books and reviews with caching",
    version="1.0"
)

# ----------------------------
# Create DB tables
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# Redis Cache using fakeredis
# ----------------------------
redis_client = fakeredis.FakeStrictRedis()
CACHE_TTL = 30  # seconds

# ----------------------------
# Database Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Book Endpoints
# ----------------------------

@app.get("/books", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    try:
        cached_books = redis_client.get("books")
        if cached_books:
            return json.loads(cached_books)

        books = crud.get_books(db)
        books_data = [schemas.Book.from_orm(book).dict() for book in books]

        redis_client.setex("books", CACHE_TTL, json.dumps(books_data))
        return books_data

    except Exception:
        books = crud.get_books(db)
        return [schemas.Book.from_orm(book) for book in books]

@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = crud.create_book(db, book)
    redis_client.delete("books")  # Invalidate cache
    return new_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: UUID, book_update: schemas.BookCreate, db: Session = Depends(get_db)):
    updated_book = crud.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    redis_client.delete("books")  # Invalidate cache
    return updated_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    deleted_book = crud.delete_book(db, book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    redis_client.delete("books")  # Invalidate cache
    return deleted_book

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: UUID, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ----------------------------
# Review Endpoints
# ----------------------------

@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
def add_review(book_id: UUID, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.add_review(db, book_id, review)

@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
def get_reviews(book_id: UUID, db: Session = Depends(get_db)):
    return crud.get_reviews(db, book_id)
