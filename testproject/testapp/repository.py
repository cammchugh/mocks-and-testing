from datetime import datetime, timedelta
from testapp.models import Book


class BookRepository(object):

    def best_sellers_last_week(self):
        last_week = datetime.now() - timedelta(days=7)
        return Book.objects.bestsellers(since=last_week)
