from datetime import datetime, timedelta
from django.db.models import Sum, Count
from testapp.dwilio import DwilioClient, BestSellerNotification
from testapp.models import Book
from testapp.repository import BookRepository


class BestsellerNotifierVersion1(object):

    def notify_current_best_sellers(self):
        dwilio_client = DwilioClient()
        last_week = datetime.now() - timedelta(days=7)
        best_sellers = Book.objects.annotate(total_sales=Sum('booksold__price'), total_sold=Count('booksold')).\
            filter(booksold__date__gte=last_week)
        for book in best_sellers:
            notification = BestSellerNotification(book)
            dwilio_client.send_notification(notification)


class BestsellerNotifierVersion2(object):

    def notify_current_best_sellers(self):
        dwilio_client = DwilioClient()
        last_week = datetime.now() - timedelta(days=7)
        best_sellers = Book.objects.bestsellers(since=last_week)
        for book in best_sellers:
            notification = BestSellerNotification(book)
            dwilio_client.send_notification(notification)


class BestsellerNotifierVersion3(object):

    def notify_current_best_sellers(self):
        dwilio_client = DwilioClient()
        best_sellers = Book.best_sellers_last_week()
        for book in best_sellers:
            notification = BestSellerNotification(book)
            dwilio_client.send_notification(notification)


class BestsellerNotifierVersion4(object):

    def __init__(self, book_repository=None, dwilio_client=None):
        self.book_repository = book_repository or BookRepository()
        self.dwilio_client = dwilio_client or DwilioClient()

    def notify_current_best_sellers(self):
        best_sellers = self.book_repository.best_sellers_last_week()
        for book in best_sellers:
            notification = BestSellerNotification(book)
            self.dwilio_client.send_notification(notification)