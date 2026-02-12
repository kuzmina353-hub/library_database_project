from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


class Gender(models.IntegerChoices):
    NOT_SPECIFIED = 0, 'Not specified'
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'
    OTHER = 3, 'Other'

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.NOT_SPECIFIED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.surname} {self.first_name}"

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Publishing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Variety(models.TextChoices):
    PAPERBACK = "PAPERBACK", 'Paperback'
    E_BOOK = "E_BOOK", 'E-Book'
    AUDIO_BOOK = "AUDIO_BOOK", 'Audiobook'


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='books')
    publishing = models.ForeignKey(Publishing, on_delete=models.SET_NULL, null=True, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    year_published = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField(default=1)
    variety = models.CharField(max_length=20,choices=Variety.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Reader(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.NOT_SPECIFIED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.surname} {self.first_name}"

class Lending(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='lendings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='lendings')
    lending_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.book.available_copies <= 0:
                raise ValidationError("No available copies.")
            self.book.available_copies -= 1
            self.book.save()
        else:
            old_copy = Lending.objects.get(pk=self.pk)
            if not old_copy.returned and self.returned:
                self.book.available_copies += 1
                self.return_date = date.today()
                self.book.save()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.reader} borrowed {self.book}"


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='phones'
    )
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.phone

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    reader = models.OneToOneField(
        Reader,
        on_delete=models.CASCADE,
        related_name='address'
    )
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=20)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    entrance = models.CharField(max_length=20, blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.city}, {self.street} {self.building}"

