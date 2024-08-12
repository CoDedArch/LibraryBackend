from ninja import Schema
from ninja import NinjaAPI, Schema
from datetime import date
from pydantic import Field, BaseModel, EmailStr
from typing import List, Optional

class ReaderSchema(Schema):
    id: int
    user_id: int


class GenreSchema(Schema):
    id: int
    genre: str
    # get_books: List

    
class SignupSchema(BaseModel):
    fullname: str
    date_of_birth: date
    city: str
    username: str
    email: EmailStr
    password: str
    confirmpassword: str


class BookSchema(Schema):
    id: int
    title: str
    book_type: str
    cover_img: str
    publication_date: date
    no_pages: Optional[int]
    LibraryId: Optional[str]
    isbn10: Optional[str]
    isbn13: Optional[str]
    publisher: Optional[str]
    genre_id: Optional[int]
    reader_id: Optional[int]
    average_rating: float
    number_of_ratings: int
    readers_currently_reading: int
    readers_finished_reading: int
    want_to: int
    total_downloads: int
    total_shares: int


class BookAuthorSchema(Schema):
    id: int
    title: str
    book_type: str
    cover_img: str
    publication_date: date
    

class ReadingStatusSchema(Schema):
    id: int
    reader_id: int
    book_id: int
    status: str


class BookActivitySchema(Schema):
    id: int
    reader_id: int
    book_id: int
    activity_type: str
    timestamp: str


class RatingSchema(Schema):
    bookId: int
    rating: float

class UserRatingSchema(Schema):
    value: float
