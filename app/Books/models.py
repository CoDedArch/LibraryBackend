from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model, UniqueConstraint

def book_dir(instance, filename):
    return f'{instance.title}/{filename}'


class Reader(Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_reader')
    fullname = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    def get_books(self):
        return Book.objects.filter(reader=self)
    
    def log_download(self, book):
        BookActivity.objects.create(reader=self, book=book, activity_type='download')

    def log_share(self, book):
        BookActivity.objects.create(reader=self, book=book, activity_type='share')


# class Author(Model):
#     name = models.CharField(max_length=150, default="John Doe")
#     email = models.EmailField(unique=True, blank=True, null=True)

#     def get_books(self):
#         return Book.objects.filter(author= self)


class Genre(Model):
    genre = models.CharField(max_length=100, verbose_name='Genre')

    def get_books(self):
        return Book.objects.filter(genre=self)
    
    def __str__(self) -> str:
        return self.genre


class Book(Model):
    class BookType(models.TextChoices):
        EBOOK = 'EB', 'E-book'
        AUDIOBOOK = 'AU', 'Audio-book'

    title = models.CharField(max_length=120, verbose_name='book title')
    book_type = models.CharField(max_length=2, choices=BookType.choices)
    cover_img = models.ImageField(upload_to=book_dir)
    publication_date = models.DateField()
    no_pages = models.IntegerField(null=True, blank=True)
    LibraryId = models.CharField(max_length=11, unique=True, verbose_name="Let's learn ID", null=True, blank=True)
    isbn10 = models.CharField(max_length=10, unique=True, verbose_name='ISBN-10', null=True, blank=True)
    isbn13 = models.CharField(max_length=13, unique=True, verbose_name='ISBN-13', null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genres', null=True, blank=True)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reader_book',null=True, blank=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.value for rating in ratings) / len(ratings)
        return 0
    def number_of_ratings(self):
        return f'{len(self.ratings.all())}'

    def readers_currently_reading(self):
        return f'{self.readingstatus_set.filter(status='reading').count()}'
    
    def readers_finished_reading(self):
        return f'{self.readingstatus_set.filter(status='finished').count()}'
    
    def readers_want_to_start_reading(self):
        return f'{self.readingstatus_set.filter(status='want to').count()}'

    def total_downloads(self):
        return f'{self.bookactivity_set.filter(activity_type='download').count()}'
    
    def total_shares(self):
        return f'{self.bookactivity_set.filter(activity_type='share').count()}'
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title','publisher'], name='unique_title_publisher')
        ]


class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('finished', 'Finished'),
        ('want to', 'Want to Read'),
    ]

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.reader.user.username} - {self.book.title} - {self.status}'


class BookActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('download', 'Download'),
        ('share', 'Share'),
    ]

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reader.user.username} {self.activity_type}ed {self.book.title} on {self.timestamp}'


class Rating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f'{self.value} for {self.book.title} by {self.reader.user.username}'