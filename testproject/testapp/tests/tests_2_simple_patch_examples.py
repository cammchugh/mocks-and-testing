from django.test import SimpleTestCase
from unittest.mock import patch

# NOTE: patch will fail if specified attribute does not exist.

def my_get_cwd():
    import os
    return os.getcwd()


class SimplePatchExamples(SimpleTestCase):

    @patch('os.getcwd')
    def test_my_get_cwd_patch_decorator(self, mock_cwd):
        mock_cwd.return_value = 'foo'
        self.assertEqual('foo', my_get_cwd())

    def test_my_get_cwd_context_manager(self):
        with patch('os.getcwd') as mock_cwd:
            mock_cwd.return_value = 'foo'
            actual_cwd = my_get_cwd()

        self.assertEqual('foo', actual_cwd)


@patch('os.getcwd')
class PatchEveryTestWithADecorator(SimpleTestCase):

    def test_cwd_foo(self, mock_cwd):
        mock_cwd.return_value = 'foo'
        self.assertEqual('foo', my_get_cwd())

    def test_cwd_bar(self, mock_cwd):
        mock_cwd.return_value = 'bar'
        self.assertEqual('bar', my_get_cwd())

    def test_cwd_baz(self, mock_cwd):
        mock_cwd.return_value = 'baz'
        self.assertEqual('baz', my_get_cwd())


class PatchEveryTestWithAPatcher(SimpleTestCase):

    def setUp(self):
        patcher = patch('os.getcwd')
        self.mock_cwd = patcher.start()
        self.addCleanup(patcher.stop)

    def test_cwd_foo(self):
        self.mock_cwd.return_value = 'foo'
        self.assertEqual('foo', my_get_cwd())

    def test_cwd_bar(self):
        self.mock_cwd.return_value = 'bar'
        self.assertEqual('bar', my_get_cwd())

    def test_cwd_baz(self):
        self.mock_cwd.return_value = 'baz'
        self.assertEqual('baz', my_get_cwd())
