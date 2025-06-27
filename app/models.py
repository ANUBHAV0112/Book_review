from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from .database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    title = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    complete = Column(Boolean, default=False)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    book_id = Column(String(36), ForeignKey("books.id"))
    content = Column(Text)
    rating = Column(String(50))

    book = relationship("Book", back_populates="reviews")
