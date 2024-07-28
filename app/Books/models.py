from django.db import models
from django.db.models import Model, UniqueConstraint

def book_dir(instance, filename):
    return f'{instance.title}/{filename}'

# Create your models here.
class Author(Model):
    name = models.CharField(max_length=100, default="John Doe")
    email = models.EmailField(unique=True, blank=True, null=True)



class Book(Model):
    class BookType(models.TextChoices):
        EBOOK = 'EB', 'E-book'
        AUDIOBOOK = 'AU', 'Audio-book'

    title = models.CharField(max_length=120, verbose_name='book title')
    book_type = models.CharField(max_length=2, choices=BookType.choices)
    cover_img = models.ImageField(upload_to=book_dir)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title','author'], name='unique_title_author')
        ]

class Genre(Model):
    genre = models.CharField(max_length=100, verbose_name='Genre')
    books = models.ForeignKey(Book, on_delete=models.CASCADE)