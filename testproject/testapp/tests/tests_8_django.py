from django.test import SimpleTestCase, TestCase
from unittest.mock import create_autospec, Mock

from ..models import Author, Book


class SpecAndDjangoModels(SimpleTestCase):

    def tests_speccing_model_classes_probably_wont_work(self):
        mock_author = Mock(spec=Author)
        book = Book()
        book.author = mock_author
        self.assertEqual(mock_author, book.author)

    def tests_speccing_model_instances_might_be_better(self):
        mock_author = Mock(spec=Author())
        book = Book()
        book.author = mock_author
        self.assertEqual(mock_author, book.author)

    def tests_autospeccing_model_class(self):
        mock_book = create_autospec(Book)
        author = mock_book.author
        another_book = Book()
        another_book.author = author
        self.assertEqual(author, another_book.author)

    def tests_autospeccing_model_instance(self):
        mock_book = create_autospec(Book()) # WTF?
        author = mock_book.author
        another_book = Book()
        another_book.author = author
        self.assertEqual(author, another_book.author)