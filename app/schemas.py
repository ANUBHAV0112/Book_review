from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class ReviewBase(BaseModel):
    content: str
    rating: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: UUID
    book_id: UUID

    class Config:
        from_attributes = True



class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    complete: bool = False

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: UUID
    reviews: List[Review] = []

    class Config:
        from_attributes = True

