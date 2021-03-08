from django.test import SimpleTestCase
from unittest.mock import Mock

from ..billing import AccountDebit, BillingSystem
from ..pay_per_use_formatter import PayPerUseStringFormatter
from ..slow_formatter import SlowStringFormatter


class InversionOfControlDependencyInjectionExample(SimpleTestCase):

    # patch is kind of gross, and with a few minor changes can help you completely avoid it.
    def test_patching_classes(self):
        # setup
        # use the mock class return_value to get the instance that will be returned under test
        mock_billing_system = Mock(spec=BillingSystem, **{
            'charge_for_usage.return_value': {
                'status_code': 200,
                'response': {'success': True, 'new_balance': 50}
            },
        })

        # If you set a another mock as class return_value, you'll need to autospec again or risk errors.
        mock_slow_formatter = Mock(spec=SlowStringFormatter, **{
            'really_slow_string_format.return_value': 'asdf',
        })

        # Pass the dependencies via the constructor.
        formatter = PayPerUseStringFormatter(
            formatter=mock_slow_formatter,
            billing_system=mock_billing_system
        )

        # execute
        new_balance, concatenated_result = formatter.concatenate('string1', 'string2', 'string3')

        # assert
        # not having a direct reference to the mock makes calling assert methods awkward though.
        mock_billing_system.charge_for_usage.assert_called_once_with(AccountDebit('AC123', 100))
        self.assertEqual(50, new_balance)
        mock_slow_formatter.really_slow_string_format.assert_called_once_with('string1', 'string2')
        self.assertEqual('asdf string3', concatenated_result)