from datetime import datetime, timedelta
from django.db import models
from django.db.models import Sum, Count


class Author(models.Model):
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32)


class BestSellerManager(models.Manager):

    def bestsellers(self, since_date):
        return self.annotate(total_sales=Sum('booksold__price'), total_sold=Count('booksold')). \
            filter(booksold__date__gte=since_date)


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    objects = BestSellerManager()

    @classmethod
    def best_sellers_last_week(cls):
        last_week = datetime.now() - timedelta(days=7)
        cls.objects.bestsellers(last_week)


class BookSold(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    price = models.IntegerField()
    date = models.DateField()
