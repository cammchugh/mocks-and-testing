from django.test import SimpleTestCase
from unittest.mock import patch, Mock

from ..billing import AccountDebit
from ..pay_per_use_formatter import PayPerUseStringFormatter

# NOTES:
# you always patch the targeted class or method where it was imported, not where it was defined.
# multiple patches are resolved "inside out", last applied patch is first param.


class PatchExamples(SimpleTestCase):

    # Replaces only the patched method, all other calls will go to actual code.
    @patch('testapp.billing.BillingSystem.charge_for_usage')
    @patch('testapp.pay_per_use_formatter.SlowStringFormatter.really_slow_string_format')
    def test_patching_methods_directly(self, slow_format_mock, charge_mock):
        # setup
        charge_mock.return_value = {
            'status_code': 200,
            'response': { 'success': True, 'new_balance': 50}
        }
        slow_format_mock.return_value = 'asdf'

        formatter = PayPerUseStringFormatter()

        # execute
        new_balance, concatenated_result = formatter.concatenate('string1', 'string2', 'string3')

        # assert
        charge_mock.assert_called_once_with(AccountDebit('AC123', 100))
        self.assertEqual(50, new_balance)
        slow_format_mock.assert_called_once_with('string1', 'string2')
        self.assertEqual('asdf string3', concatenated_result)

    # Patches the entire class, so you have to tell the class what to return. Class is entirely replaced.
    @patch('testapp.billing.BillingSystem', autospec=True)
    @patch('testapp.pay_per_use_formatter.SlowStringFormatter', autospec=True)
    def test_patching_classes(self, mock_formatter_class, mock_billing_system_class):
        # setup
        # use the mock class return_value to get the instance that will be returned under test
        mock_billing_system_class.return_value.configure_mock(**{
            'charge_for_usage.return_value': {
                'status_code': 200,
                'response': {'success': True, 'new_balance': 50}
            },
            # 'does_not_exist.return_value': 'foo' <-- would cause an exception
        })
        # If you set a another mock as class return_value, you'll need to autospec again or risk errors.
        mock_formatter = Mock(**{
            'really_slow_string_format.return_value': 'asdf',
            'does_not_exist.return_value': 'foo' # <-- Oh no, this works.
        })
        mock_formatter_class.return_value = mock_formatter

        formatter = PayPerUseStringFormatter()

        # execute
        new_balance, concatenated_result = formatter.concatenate('string1', 'string2', 'string3')

        # assert
        # not having a direct reference to the mock makes calling assert methods awkward though.
        mock_billing_system_class.return_value.charge_for_usage.assert_called_once_with(AccountDebit('AC123', 100))
        self.assertEqual(50, new_balance)
        mock_formatter.really_slow_string_format.assert_called_once_with('string1', 'string2')
        self.assertEqual('asdf string3', concatenated_result)
