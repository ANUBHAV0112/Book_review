# 📚 Book Review API

A simple FastAPI project to manage books and reviews with MySQL and Redis (using fakeredis for caching).

---

## 🚀 Features

- Create, read, update, delete (**CRUD**) books.
- Add and get reviews for a book.
- Data stored in MySQL.
- Results cached in Redis (`fakeredis`).
- Tested with Postman & MySQL Workbench.

---

## ⚙️ Technologies

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **pymysql**
- **fakeredis** (in-memory Redis for testing)

---

## 📁 Project Structure


## 🔑 Setup Instructions

1️⃣ **Clone the project**

```bash
git clone <your-repo-url>
cd Book\ review
2️⃣ Install dependencies

pip install fastapi uvicorn sqlalchemy pymysql fakeredis pydantic

3️⃣ Configure database

Update SQLALCHEMY_DATABASE_URL in database.py:

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://<username>:<password>@localhost:3306/book_review_db"

4️⃣ Start the server

uvicorn app.main:app --reload

5️⃣ Test in browser

Open: http://127.0.0.1:8000/docs

✅ API Endpoints
📚 Books
GET /books — Get all books (uses cache)

POST /books — Create a book

PUT /books/{book_id} — Update a book

DELETE /books/{book_id} — Delete a book

GET /books/{book_id} — Get a single book

📝 Reviews
POST /books/{book_id}/reviews — Add review to a book

GET /books/{book_id}/reviews — Get all reviews for a book

⚡ Example Request
Create a book

json
Copy
Edit
POST /books
{
  "title": "Solo Leveling",
  "description": "A great novel",
  "complete": true
}
🗃️ Database
Uses MySQL — table names: books, reviews.

UUID used for primary keys.

Relationships: One book has many reviews.

✅ Notes
Fakeredis simulates Redis — no need to install actual Redis.

Use Postman to test CRUD operations.

Confirm data in MySQL Workbench.

👨‍💻 Author
Anubhav Choudhary

LinkedIn | GitHub

