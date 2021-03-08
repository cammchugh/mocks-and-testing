from django.test import SimpleTestCase
from unittest.mock import patch

# Let's look at a horrible abuse of mocking, and just generally bad testing practice.

# Some made up production code.
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
    pass  # does a db insert


# This is what we want to test.
def call_all_the_methods_and_return_the_sum():
    value = call_an_api()
    foo = make_a_foo(value)
    save_to_database(foo)


class TestDrivenTheatre(SimpleTestCase):
    """
    This is what might typically call a "fantasy test".
    It's only testing the collaborator integration, everything is mocked.
    Can't change a line of code in the method under test without updating the test.
    Steve Freeman (Growing OO Software, Guided by Tests) calls this an MD5 test.
    Only exists to achieve 100% coverage, no test really needed here.
    This hurts your code base, don't do it.
    """
    def test_that_we_have_one_hundred_percent_coverage(self):
        with patch(f'{__name__}.call_an_api') as api_mock:
            with patch(f'{__name__}.make_a_foo') as foo_mock:
                with patch(f'{__name__}.save_to_database') as db_mock:
                    call_all_the_methods_and_return_the_sum()

        api_mock.assert_called_once()
        foo_mock.assert_called_once_with(api_mock.return_value)
        db_mock.assert_called_once_with(foo_mock.return_value)


# Don't couple tests to implementation details by mocking things that aren't in the public contract.
class ThisIsAlsoBad(SimpleTestCase):
    """
    Pseudo privates tend to be an implementation detail, and when mocked in a test, lead to a high degree of coupling
    between the test and the implementation. Otherwise known as "over specified".

    Generally, patching methods/attributes of a Class Under Test to test other methods/attributes is a bad idea.
    Isolate the bad dependencies and inject them as constructor or method params.
    """

    def test_test_slow_formatter_by_poking_into_internals(self):
        from ..slow_formatter import SlowStringFormatter

        slow_formatter = SlowStringFormatter()

        with patch.object(SlowStringFormatter, '_this_is_the_slow_part') as slow_mock:
            self.assertEqual('a b', slow_formatter.really_slow_string_format('a', 'b'))
