from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email_address = models.EmailField()


class Book(models.Model):
    title = models.CharField(max_length=128)
    isbn = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Library(models.Model):
    name = models.CharField(max_length=128)


class Catalog(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)