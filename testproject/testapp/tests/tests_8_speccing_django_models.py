from django.test import SimpleTestCase
from unittest.mock import create_autospec, Mock

from ..models import Author, Book


# spec and create_autospec doesn't mix very well with Django
# fortunately we probably don't need to worry about this too much with models, but what about managers and query sets?
class SpecAndDjangoModels(SimpleTestCase):

    # Raises AttributeError: Mock object has no attribute '_state'
    def tests_speccing_model_classes_probably_doesnt_really_work(self):
        mock_author = Mock(spec=Author)
        book = Book()
        book.author = mock_author
        self.assertEqual(mock_author, book.author)

    # Speccing works now, but creating an throw away instance feels dirty.
    # Will probably still fail somehow with more complex models with many relationships.
    def tests_speccing_model_instances_might_work(self):
        mock_author = Mock(spec=Author())
        book = Book()
        book.author = mock_author
        self.assertEqual(mock_author, book.author)

    # specs id, isbn, and title, but not author
    def tests_autospeccing_model_class_misses_some_stuff(self):

        mock_book = create_autospec(Book)
        author = mock_book.author
        another_book = Book()
        another_book.author = author
        self.assertEqual(author, another_book.author)

    # Raises an exception. I assume it's exercising some side effect during speccing.
    def tests_autospeccing_model_instance_plain_old_breaks(self):
        mock_book = create_autospec(Book()) # WTF?
        author = mock_book.author
        another_book = Book()
        another_book.author = author
        self.assertEqual(author, another_book.author)





