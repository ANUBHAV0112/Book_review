from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base

# ✅ Use a file-based SQLite DB for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./book_review_db_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Create tables for test DB
Base.metadata.create_all(bind=engine)

# ✅ Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books",
        json={"title": "Test Book", "description": "A book for testing", "complete": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_book():
    books = client.get("/books").json()
    book_id = books[0]["id"]

    response = client.put(
        f"/books/{book_id}",
        json={"title": "Updated Title", "description": "Updated", "complete": True}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_add_review():
    books = client.get("/books").json()
    book_id = books[0]["id"]

    response = client.post(
        f"/books/{book_id}/reviews",
        json={"content": "Nice book!", "rating": "5 stars"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Nice book!"


def test_get_reviews():
    books = client.get("/books").json()
    book_id = books[0]["id"]

    response = client.get(f"/books/{book_id}/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_book():
    books = client.get("/books").json()
    book_id = books[0]["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
