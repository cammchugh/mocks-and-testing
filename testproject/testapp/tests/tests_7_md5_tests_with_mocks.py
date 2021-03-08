from django.test import SimpleTestCase
from unittest.mock import patch

class Foo(object):

    def __init__(self, value):
        self.value = value


def call_an_api():
    return {
        'status_code': 200,
        'response': {'some': 'value'}
    }


def make_a_foo(value):
    return Foo(value)


def save_to_database(foo):
    # does a db insert
    pass


def call_all_the_methods_and_return_the_sum():
    value = call_an_api()
    foo = make_a_foo(value)
    save_to_database(foo)


"""
Steve Freeman:

"""

class TestDrivenTheatre(SimpleTestCase):

    def test_call_all_the_methods_and_return_the_sum_with_an_md5_test(self):

        with patch(f'{__name__}.call_an_api') as api_mock:
            with patch(f'{__name__}.make_a_foo') as foo_mock:
                with patch(f'{__name__}.save_to_database') as db_mock:
                    call_all_the_methods_and_return_the_sum()

        api_mock.assert_called_once()
        foo_mock.assert_called_once_with(api_mock.return_value)
        db_mock.assert_called_once_with(foo_mock.return_value)





