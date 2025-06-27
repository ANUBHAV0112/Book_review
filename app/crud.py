from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas

def get_books(db: Session):
    return db.query(models.Book).all()

def get_book(db: Session, book_id: UUID):
    return db.query(models.Book).filter(models.Book.id == str(book_id)).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: UUID):
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book

def update_book(db: Session, book_id: UUID, book_data: schemas.BookCreate):
    book = get_book(db, book_id)
    if book:
        for field, value in book_data.dict().items():
            setattr(book, field, value)
        db.commit()
        db.refresh(book)
    return book

def add_review(db: Session, book_id: UUID, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, book_id: UUID):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()
