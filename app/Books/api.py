from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.shortcuts import get_object_or_404
from .schemas import (ReaderSchema, GenreSchema,
                      BookSchema, ReadingStatusSchema, 
                      BookActivitySchema, RatingSchema, 
                      BookAuthorSchema,BookContentSchema)
from .models import (Reader, Genre, Book, ReadingStatus, 
                     BookActivity, Rating, Heading, SubHeading)
from django.http import FileResponse, Http404

# from .utils import get_pdf_pages_as_text


router = Router()

# API Endpoints
@router.get("/readers", response=List[ReaderSchema])
def list_readers(request):
    readers = Reader.objects.all()
    return readers

@router.get("/{book_id}/content", auth=JWTAuth(), response=List[dict])
def get_book_content(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise {"error": "Book not Found"}
    
    headings = Heading.objects.filter(book = book)
    book_content =  []
    for heading in headings:
        SubHeadings = SubHeading.objects.filter(heading=heading)
        heading_data = {
            "heading_id": heading.id,
            "heading_name": heading.title,
            "heading_content": heading.heading_content if heading.has_content() else "",
            "heading_image": request.build_absolute_uri(heading.heading_image.url)  if  heading.has_image() else "",
            "subheadings": [
                {
                    "subheading_id": sub.id,
                    "subheading_name": sub.title,
                    "subheading_content": sub.subheading_content if sub.has_content() else "",
                    "subheading_image": request.build_absolute_uri(sub.heading_image.url)  if  sub.has_image() else ""
                } for sub in SubHeadings
            ]
        }
        book_content.append(heading_data)
    return book_content


# def get_book_pages(request, book_id):
#     try:
#         book = Book.objects.get(id=book_id)
#         pages_text = get_pdf_pages_as_text(book)
#         return {"pages": pages_text}
#     except Book.DoesNotExist:
#         return {"error": "Book not found"}


@router.post("/book/rating", auth=JWTAuth())
def rate_a_book(request, payload: RatingSchema):
    try:
        user = request.user
        reader, created = Reader.objects.get_or_create(user=user)

        existing_rating = Rating.objects.filter(book_id=payload.bookId, reader=reader).first()
        if existing_rating:
            # Update the existing rating
            existing_rating.value = payload.rating
            existing_rating.save()
            return {"message": "Rating updated successfully!", "rating": existing_rating.value}

        # Create a new Rating instance
        rating = Rating.objects.create(
            book_id=payload.bookId,
            reader=reader,
            value=payload.rating,
        )
        return {"message": "Rating saved successfully!", "rating": rating.value}
    except Exception as e:
        return {"error": str(e)}


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
    
# @router.get("/book/{book_id}/pages")
# def get_book_pages(request, book_id: int):
#     try:
#         book = Book.objects.get(id=book_id)
#         pages = get_pdf_pages(book)
#         return {"pages": pages}
#     except Book.DoesNotExist:
#         return {"error": "Book does not exist"}

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

@router.get("/publisher/{book_id}/{publisher}", response=List[BookAuthorSchema])
def list_books_by_genre(request,book_id,publisher: str):
    books = Book.objects.filter(publisher=publisher).exclude(id = book_id)
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

@router.get("/user/ratings/{book_id}", auth=JWTAuth())
def get_user_ratings_for_book(request, book_id: int):
    try:
        user = request.user
        reader, created = Reader.objects.get_or_create(user=user)

        # Retrieve ratings for the specified book by the current user
        user_ratings = Rating.objects.filter(book_id=book_id, reader=reader)

        print(user_ratings)

        # You can further process or serialize the ratings as needed
        serialized_ratings = [{"value": rating.value} for rating in user_ratings]

        print(serialized_ratings)

        return {"user_ratings": serialized_ratings}
    except Exception as e:
        return {"error": str(e)}