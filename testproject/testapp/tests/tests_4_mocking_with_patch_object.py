from django.test import SimpleTestCase
from unittest.mock import patch

import testapp.billing
from ..pay_per_use_formatter import PayPerUseStringFormatter, SlowStringFormatter


class PatchObjectExamples(SimpleTestCase):

    # If you already have a reference to the class, then you can patch the actual class, instead of a path.
    # Requires a attribute name to patch.
    @patch.object(testapp.billing.BillingSystem, 'charge_for_usage')
    @patch.object(SlowStringFormatter, 'really_slow_string_format')
    def test_patching_classes(self, slow_format_mock, charge_mock):
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
        charge_mock.assert_called_once_with(testapp.billing.AccountDebit('AC123', 100))
        self.assertEqual(50, new_balance)
        slow_format_mock.assert_called_once_with('string1', 'string2')
        self.assertEqual('asdf string3', concatenated_result)


