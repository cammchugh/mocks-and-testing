from django.test import SimpleTestCase
from unittest.mock import call, create_autospec, ANY, Mock, MagicMock


class SimpleMockExamples(SimpleTestCase):

    def test_simple_mock_example(self):
        mock = Mock()
        mock.foo = 'foo'
        mock.bar.return_value = 1
        # assert expected values
        self.assertEquals('foo', mock.foo)
        self.assertEquals(1, mock.bar())
        # anything else returns a new mock.
        x = mock.whatever
        self.assertEquals(ANY, x)
        y = mock.doesnt_matter()
        self.assertEquals(ANY, y)

    def test_mock_assertions(self):
        mock = Mock()
        mock.some_method(1, 2, value=3)

        # was it called
        self.assertTrue(mock.some_method.called)
        # how many times it was called
        self.assertEquals(1, mock.some_method.call_count)
        # how was it called
        self.assertEquals(call(1, 2, value=3), mock.some_method.call_args)

        # more concisely
        mock.some_method.assert_called()
        mock.some_method.assert_called_once()
        mock.some_method.assert_called_once_with(1, 2, value=3)

    def test_negative_assertions(self):
        mock = Mock()
        # was it called
        self.assertFalse(mock.some_method.called)
        # how many times it was called
        self.assertEquals(0, mock.some_method.call_count)
        # more concisely, but only python >= 3.5
        mock.some_method.assert_not_called()

    def test_mock_assertions_multiple_calls_with_call_args(self):
        mock = Mock()
        mock.some_method(1, 2, value=3)
        mock.some_method(4, 5, value=6)
        # nope
        self.assertEquals(call(1, 2, value=3), mock.some_method.call_args)

    def test_mock_assertions_multiple_calls_with_called_with(self):
        mock = Mock()
        mock.some_method(1, 2, value=3)
        mock.some_method(4, 5, value=6)
        # still nope
        mock.some_method.assert_called_with(1, 2, value=3)

    def test_mock_assertions_multiple_calls_args_list(self):
        mock = Mock()
        mock.some_method(1, 2, value=3)
        mock.some_method(4, 5, value=6)

        self.assertEquals(
            call(1, 2, value=3),
            mock.some_method.mock_calls[0]
        )
        self.assertEquals(
            call(4, 5, value=6),
            mock.some_method.mock_calls[1]
        )

    def test_mock_assertions_multiple_calls_any(self):
        mock = Mock()
        mock.some_method(1, 2, value=3)
        mock.some_method(4, 5, value=6)
        # maybe we don't care about order
        mock.some_method.assert_any_call(4, 5, value=6)
        mock.some_method.assert_any_call(1, 2, value=3)

    def test_some_internal_details_of_a_mock(self):
        mock = Mock()
        mock.some_method(1, 2, value=3)
        mock.some_method(4, 5, value=6)

        # call_args only stores most recent call
        self.assertEquals(call(4, 5, value=6), mock.some_method.call_args)

        # call_args_list stores all calls, in order received
        self.assertEquals(
            [
                call(1, 2, value=3),
                call(4, 5, value=6)
            ],
            mock.some_method.call_args_list
        )

        # 'call' is just a wrapper around tuple
        args, kwargs = mock.some_method.call_args
        self.assertEquals((4, 5), args)
        self.assertEquals({'value': 6}, kwargs)

        # but calls in the base mock's mock_calls/method_calls are different, they include the name of the callable.
        name, args, kwargs = mock.mock_calls[0]
        self.assertEquals('some_method', name)
        self.assertEquals((1, 2), args)
        self.assertEquals({'value': 3}, kwargs)

    def test_assert_called_with_object_fails_due_to_reference_equality(self):

        class MyObject(object):
            def __init__(self, attr1):
                self.attr1 = attr1

        mock = Mock()

        # application code
        actual_arg_obj = MyObject(1)
        actual_kwarg_obj = MyObject(2)
        mock.method_with_object_param(actual_arg_obj, kwarg_obj=actual_kwarg_obj)

        # test code
        expected_arg_obj = MyObject(1)
        expected_kwarg_obj = MyObject(2)
        # this won't work, maybe you should implement __eq__?
        mock.method_with_object_param.assert_called_once_with(expected_arg_obj, kwarg_obj=expected_kwarg_obj)

    def test_assert_called_with_object_assert_on_attributes_of_call_args_instead(self):

        class MyObject(object):
            def __init__(self, attr1):
                self.attr1 = attr1

        mock = Mock()

        # application code
        actual_arg_obj = MyObject(1)
        actual_kwarg_obj = MyObject(2)
        mock.method_with_object_param(actual_arg_obj, kwarg_obj=actual_kwarg_obj)

        # you can dig into the calls to get the args, but it gets messy quickly so avoid unless you *really* need it.
        mock.method_with_object_param.assert_called_once()
        actual_call = mock.method_with_object_param.mock_calls[0]
        self.assertEqual(1, actual_call.args[0].attr1)
        self.assertEqual(2, actual_call.kwargs['kwarg_obj'].attr1)

    def test_magic_mock(self):
        mock = Mock()
        # nope
        with self.assertRaises(TypeError):
            self.assertEqual(1, int(mock))

        # still nope
        with self.assertRaises(AttributeError):
            mock.__int__.return_value = 1

        # MagicMock to the rescue
        magic_mock = MagicMock()
        self.assertEqual(1, int(magic_mock))
        # defaults supplied for all magic methods, but you can override.
        magic_mock.__int__.return_value = 3
        self.assertEqual(3, int(magic_mock))
        magic_mock.__iter__.return_value = iter([1, 2])
        self.assertEquals([1, 2], list(magic_mock))
        magic_mock.__bool__.return_value = False
        self.assertFalse(bool(magic_mock))
        magic_mock.__str__.return_value = 'asdf'
        self.assertEquals('asdf', str(magic_mock))
        # and more, look at the docs

    def test_common_pitfalls(self):
        mock = Mock()
        # a mock is truthy
        self.assertTrue(mock.foo)
        # typos FTW
        mock.foo.asssert_called_once()

    def test_spec_to_the_rescue(self):

        class MyClass(object):
            foo = 'foo'

            def bar(self):
                return 'bar'

        mock = Mock(spec=MyClass)

        self.assertTrue(isinstance(mock, MyClass))

        with self.assertRaises(AttributeError):
            self.assertTrue(mock.bleep)

        with self.assertRaises(AttributeError):
            self.assertTrue(mock.bloop())

        # the usual stuff works the same way
        mock.bar.return_value = 'asdf'
        self.assertEqual('asdf', mock.bar())

        # still typos FTW, though
        mock.bar.asssert_called_once()

        # and you can still screw it up a bit too.
        mock.not_a_real_attribute = 5
        self.assertEqual(5, mock.not_a_real_attribute)

    def test_autospec_turtles_all_the_way_down(self):

        class MyClass(object):
            foo = 'foo'

            def bar(self):
                return 'bar'

        # create_autospec introspects class and attempts to add appropriate mock responses.
        # be careful, introspection can sometimes have side effects
        mock = create_autospec(MyClass)

        # now we're ok
        with self.assertRaises(AttributeError):
            mock.bar.asssert_called_once()

        # use spec_set to prevent writing invalid attributes
        mock = create_autospec(MyClass, spec_set=True)

        # now we're ok
        with self.assertRaises(AttributeError):
            mock.not_an_attribute = 5

    def test_auto_spec_limitations(self):

        class MyClass(object):
            def __init__(self):
                self.foo = 'bar'

        mock = create_autospec(MyClass)

        # oops, autospec only introspects class attributes, not instance variables
        with self.assertRaises(AttributeError):
            _ = mock.foo

        # you can add them after, but remember... not if you use spec_set=True
        mock.foo = 'asdf'
        self.assertEqual('asdf', mock.foo)
        # Docs say you can use an instance in the spec, or subclass your production class and add class level
        # defaults. Not sure I love either of those options.

    def test_raising_an_exception(self):

        mock = Mock()
        mock.goes_boom.side_effect = Exception('Boom')

        with self.assertRaises(Exception) as ex_context:
            mock.goes_boom()

        self.assertEquals('Boom', str(ex_context.exception))

    def test_multiple_return_values(self):

        mock = Mock()
        mock.return_an_integer.side_effect = [1, 2, 3]

        value1 = mock.return_an_integer()
        value2 = mock.return_an_integer()
        value3 = mock.return_an_integer()

        self.assertEquals([1, 2, 3], [value1, value2, value3])

        # walking off the end raises StopIteration
        with self.assertRaises(StopIteration):
            mock.return_an_integer()

    def test_methods_of_initialization(self):

        # basic constructor params
        mock1 = Mock(the_answer=42, return_value='thanks for all the fish')
        self.assertEquals(42, mock1.the_answer)
        self.assertEquals('thanks for all the fish', mock1())

        # use a dictionary for non-trivial setup
        return_values = [1, 2, 3]
        mock_attrs = {
            'return_an_integer.side_effect': return_values,
            'goes_boom.side_effect': Exception('Boom'),
            'returns_a_value.return_value': 50
        }
        mock2 = Mock(**mock_attrs)

        self.assertEqual(1, mock2.return_an_integer())
        self.assertEqual(2, mock2.return_an_integer())
        self.assertEqual(3, mock2.return_an_integer())
        with self.assertRaises(Exception) as ex_context:
            mock2.goes_boom()
        self.assertEqual('Boom', str(ex_context.exception))
        self.assertEqual(50, mock2.returns_a_value())

        # or use configure_mock, only really necessary when initialization can't be completed at construction
        mock3 = Mock()
        mock3.configure_mock(**mock_attrs)
        self.assertEqual(1, mock3.return_an_integer())
        # ...and so on
