from ninja import Router
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reader
from .schemas import SignupSchema, ReaderInfoSchema, BookSchema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth


router = Router()

@router.post("/create_reader", response=dict)
def create_user(request, payload:SignupSchema):
    try:
        user = User.objects.create_user(
            username=payload.username, 
            password=payload.password, 
            email=payload.email
        )
        reader = Reader.objects.create(
            user=user, fullname=payload.fullname, 
            date_of_birth=payload.date_of_birth, 
            city=payload.city
        )
        return {"ok": True, "user_id": user.id}
    except IntegrityError:
        raise HttpError(500, "Username or email already exists.")
    
    except ValidationError as e:
        raise HttpError(400, f"Validation error: {str(e)}")
    

@router.get("/reader-info",response= dict, auth=JWTAuth())
def get_reader_info(request):
    try:
        reader = Reader.objects.get(user=request.auth.id)
        print(reader)
        # books_read = reader.get_books()
        
        # if books_read:
        #     total_books_read = len(books_read)
        #     book_schemas = [
        #     BookSchema(
        #         id=book.id,
        #         title=book.title,
        #         book_type=book.book_type,
        #         cover_img=book.cover_img,publication_date=book.publication_date,
        #         no_pages=book.no_pages,
        #         LibraryId=book.LibraryId,
        #         isbn10=book.isbn10,
        #         isbn13=book.isbn13,
        #         publisher=book.publisher,
        #         genre_id=book.genre_id,
        #         reader_id=book.reader_id,
        #         average_rating=book.average_rating,
        #         number_of_ratings=book.number_of_ratings,
        #     )
        #     for book in books_read
        # ]
        print(request.auth.username)
        return {
            "ok":True, "username": request.auth.username,
        }
    except Reader.DoesNotExist:
        return {
            "ok":True, "username": request.auth.username,
        }
