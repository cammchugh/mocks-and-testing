from django.test import SimpleTestCase

from ..models import Book
from ..notifiers import BestsellerNotifierVersion4


# This relies on the "Repository Pattern", whose goal is to abstract details of storage.
# The idea is that your domain logic only sees in "in memory" collection of objects.
# This isn't common in Python, and all but unheard of in Django (for good reason?).
# But, let's just see what this would look like...
class FakeRepository(object):

    def __init__(self, books):
        self.books = books

    def best_sellers_last_week(self):
        return self.books


class FakeDwilioClient(object):
    _notifications = []

    def send_notification(self, notification):
        self._notifications.append(notification)


# No mocking or patching here.
# Are fakes better than mocks? I'm on the fence. Both have a cost, both need to be maintained.
class TestBestSellerNotifierNoPatching(SimpleTestCase):

    def test_best_seller_notifications_using_dependency_injection(self):
        # setup
        fake_client = FakeDwilioClient()
        books = [Book('Book1'), Book('Book3')]
        fake_repo = FakeRepository(books)
        sender = BestsellerNotifierVersion4(
            dwilio_client=fake_client,
            book_repository=fake_repo,
        )
        # execute
        sender.notify_current_best_sellers()
        # assert
        self.assertEqual(2, len(fake_client._notifications))
        self.assertEqual(books[0], fake_client._notifications[0].book)
        self.assertEqual(books[1], fake_client._notifications[1].book)