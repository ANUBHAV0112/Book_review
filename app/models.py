from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.mysql import CHAR as SQLUUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from .database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(SQLUUID(36), primary_key=True, default=uuid4, index=True)
    title = Column(String(255), index=True)   # ✅ add length!
    description = Column(Text, nullable=True)
    complete = Column(Boolean, default=False)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(SQLUUID(36), primary_key=True, default=uuid4)
    book_id = Column(SQLUUID(36), ForeignKey("books.id"))
    content = Column(Text)
    rating = Column(String(50))  # ✅ add length here too!

    book = relationship("Book", back_populates="reviews")
