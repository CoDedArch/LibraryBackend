from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.shortcuts import get_object_or_404
from .schemas import (ReaderSchema, GenreSchema,
                      BookSchema, ReadingStatusSchema, 
                      BookActivitySchema, RatingSchema, 
                      BookAuthorSchema)
from .models import (Reader, Genre, Book, ReadingStatus, 
                     BookActivity, Rating)
from django.http import FileResponse, Http404
from .utils import get_pdf_pages

router = Router()

# API Endpoints
@router.get("/readers", response=List[ReaderSchema])
def list_readers(request):
    readers = Reader.objects.all()
    return readers

@router.get("/download_book/{book_id}",auth=JWTAuth())
def download_book(request, book_id: int):
    try:
        user = request.user
        reader, created = Reader.objects.get_or_create(user=user)
        # retrieve book by id
        book = Book.objects.get(id=book_id)
        # create a Book activity instance 
        BookActivity.objects.create(reader=reader, book=book, activity_type='download')
        # return book as a fileResponse
        response = FileResponse(book.pdf_file.open(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
        return response
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    
@router.get("/book/{book_id}/pages")
def get_book_pages(request, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
        pages = get_pdf_pages(book)
        return {"pages": pages}
    except Book.DoesNotExist:
        return {"error": "Book does not exist"}

@router.get("/genres", response=List[GenreSchema])
def list_genres(request):
    genres = Genre.objects.all()
    return genres

@router.get("/books/genre/{genre}", response=List[BookSchema])
def list_books_by_genre(request, genre: int):
    books = Book.objects.filter(genre=genre)
    return [
        {
            "id": book.id,
            "title": book.title,
            "book_type": book.book_type,
            "cover_img": request.build_absolute_uri(book.cover_img.url) if book.cover_img else None,
            "publication_date": book.publication_date,
            "no_pages": book.no_pages,
            "LibraryId": book.LibraryId,
            "isbn10": book.isbn10,
            "isbn13": book.isbn13,
            "publisher": book.publisher,
            "genre_id": book.genre.id if book.genre else None,
            "reader_id": book.reader.id if book.reader else None,
            "average_rating": book.average_rating(),
            "number_of_ratings": book.number_of_ratings(),
            "readers_currently_reading": book.readers_currently_reading(),
            "readers_finished_reading": book.readers_finished_reading(),
            "want_to": book.readers_want_to_start_reading(),
            "total_downloads": book.total_downloads(),
            "total_shares": book.total_shares(),
        }
        for book in books
    ]

@router.get("/publisher/{publisher}", response=List[BookAuthorSchema])
def list_books_by_genre(request, publisher: str):
    books = Book.objects.filter(publisher=publisher)
    return [
        {
            "id": book.id,
            "title": book.title,
            "book_type": book.book_type,
            "cover_img": request.build_absolute_uri(book.cover_img.url) if book.cover_img else None,
            "publication_date": book.publication_date
        }
        for book in books
    ]

@router.get("/{book_id}", response=BookSchema)
def a_book(request, book_id:int):
    book = get_object_or_404(Book, id=book_id)
    return {
        "id": book.id,
        "title": book.title,
        "book_type": book.book_type,
        "cover_img": request.build_absolute_uri(book.cover_img.url) if book.cover_img else None,
        "publication_date": book.publication_date,
        "no_pages": book.no_pages,
        "LibraryId": book.LibraryId,
        "isbn10": book.isbn10,
        "isbn13": book.isbn13,
        "publisher": book.publisher,
        "genre_id": book.genre.id if book.genre else None,
        "reader_id": book.reader.id if book.reader else None,
        "average_rating": book.average_rating(),
        "number_of_ratings": book.number_of_ratings(),
        "readers_currently_reading": book.readers_currently_reading(),
        "readers_finished_reading": book.readers_finished_reading(),
        "want_to": book.readers_want_to_start_reading(),
        "total_downloads": book.total_downloads(),
        "total_shares": book.total_shares()
    }

@router.get("", response=List[BookSchema])
def list_books(request):
    books = Book.objects.all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "book_type": book.book_type,
            "cover_img": book.cover_img.url if book.cover_img else None,
            "publication_date": book.publication_date,
            "no_pages": book.no_pages,
            "LibraryId": book.LibraryId,
            "isbn10": book.isbn10,
            "isbn13": book.isbn13,
            "publisher": book.publisher,
            "genre_id": book.genre.id if book.genre else None,
            "reader_id": book.reader.id if book.reader else None,
            "average_rating": book.average_rating(),
            "number_of_ratings": book.number_of_ratings(),
            "readers_currently_reading": book.readers_currently_reading(),
            "readers_finished_reading": book.readers_finished_reading(),
            "want_to": book.readers_want_to_start_reading(),
            "total_downloads": book.total_downloads(),
            "total_shares": book.total_shares(),
        }
        for book in books
    ]

@router.get("/reading-statuses", response=List[ReadingStatusSchema])
def list_reading_statuses(request):
    statuses = ReadingStatus.objects.all()
    return statuses

@router.get("/book-activities", response=List[BookActivitySchema])
def list_book_activities(request):
    activities = BookActivity.objects.all()
    return activities

@router.get("/ratings", response=List[RatingSchema])
def list_ratings(request):
    ratings = Rating.objects.all()
    return ratings
