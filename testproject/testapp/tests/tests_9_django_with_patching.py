from datetime import datetime, timedelta
from django.test import SimpleTestCase, TestCase
from unittest.mock import patch, ANY

from ..models import Author, Book, BookSold
from ..notifiers import BestsellerNotifierVersion1, \
    BestsellerNotifierVersion2, \
    BestsellerNotifierVersion3


# We more or less have to patch the part that calls an API, but we can set up the DB in the expected start state.
# Not using factories, so this is more verbose than it needs to be.
# Either way, this still feels like setting up mock expectations and can result in an "over specified test".
# Don't try to mock query set construction, every time you do it a kitten dies.
class TestBestSellerNotifierUsingDB(TestCase):

    def test_notify_best_sellers_using_orm_and_patching_client(self):
        # setup
        today = datetime.now()
        two_weeks_ago = today - timedelta(days=14)
        # cam's book
        cam = Author.objects.create(name='Cam McHugh', phone_number='+13065551111')
        cams_book = Book.objects.create(title='Do This', author=cam)
        BookSold.objects.create(book=cams_book, price=10, date=today)
        BookSold.objects.create(book=cams_book, price=8, date=today)
        BookSold.objects.create(book=cams_book, price=10, date=two_weeks_ago)
        BookSold.objects.create(book=cams_book, price=8, date=two_weeks_ago)
        # brennan's book
        brennan = Author.objects.create(name='Brennan Rauert', phone_number='+13065552222')
        brennans_book = Book.objects.create(title='Don\'t Do That', author=brennan)
        BookSold.objects.create(book=brennans_book, price=8, date=two_weeks_ago)
        # teresa's book
        teresa = Author.objects.create(name='Teresa Hume', phone_number='+13065553333')
        teresas_book = Book.objects.create(title='Cam and Brennan are both wrong', author=teresa)
        BookSold.objects.create(book=teresas_book, price=10, date=today)
        BookSold.objects.create(book=teresas_book, price=8, date=today)
        BookSold.objects.create(book=teresas_book, price=8, date=today)
        BookSold.objects.create(book=teresas_book, price=8, date=today)
        BookSold.objects.create(book=teresas_book, price=10, date=two_weeks_ago)
        BookSold.objects.create(book=teresas_book, price=8, date=two_weeks_ago)

        with patch('testapp.notifiers.DwilioClient.send_notification') as mock_send:
            sender = BestsellerNotifierVersion1()
            sender.notify_current_best_sellers()

        self.assertEqual(2, mock_send.call_count)
        # ... more assertions over mock args list, won't be pretty


# If we're willing to restructure the code and push the query implementation into a manager, query set,
# class method, etc. then we have the start of a "seam" that allows us to mock a behaviour instead of an implementation.
class TestBestSellerNotifierWithoutUsingDB(SimpleTestCase):

    # patch the book manager
    def test_best_seller_notifications_using_patch_for_both_manager_and_client(self):
        # setup
        books = [Book('Book1'), Book('Book3')]

        with patch('testapp.notifiers.DwilioClient.send_notification') as mock_send:
            with patch('testapp.notifiers.Book.objects.bestsellers') as mock_bestsellers:
                mock_bestsellers.return_value = books
                sender = BestsellerNotifierVersion2()
                sender.notify_current_best_sellers()

        self.assertEqual(2, mock_send.call_count)
        # ... more assertions over mock args list
        mock_bestsellers.assert_called_once_with(since=ANY) # I'm lazy

    # Patch the Book class method.
    # I think I prefer this over patching managers, as it couples to the fewest details and only involves the
    # established, public contract of the book class.
    def test_best_seller_notifications_using_patch_client_and_class_method(self):
        # setup
        books = [Book('Book1'), Book('Book3')]

        with patch('testapp.notifiers.DwilioClient.send_notification') as mock_send:
            with patch('testapp.notifiers.Book.best_sellers_last_week') as mock_bestsellers:
                mock_bestsellers.return_value = books
                sender = BestsellerNotifierVersion3()
                sender.notify_current_best_sellers()

        self.assertEqual(2, mock_send.call_count)
        # ... more assertions over mock args list
        mock_bestsellers.assert_called_once() # Don't have to worry about date any more