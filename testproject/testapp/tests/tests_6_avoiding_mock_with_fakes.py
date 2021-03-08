from django.test import SimpleTestCase
from unittest.mock import patch

from ..billing import AccountDebit
from ..pay_per_use_formatter import PayPerUseStringFormatter
from ..slow_formatter import SlowStringFormatter


# A complete stub/fake object
class FakeBillingSystem(object):
    _debit = None

    def charge_for_usage(self, debit):
        self._debit = debit
        return {
            'status_code': 200,
            'response': {'success': True, 'new_balance': 50}
        }


# Override production class to remove undesirable behaviour.
# This is a bit sus though, still couples to implementation details.
class FakeFormatter(SlowStringFormatter):

    def _this_is_the_slow_part(self):
        pass

# With our previous change to "inject" dependencies, we can pass Fakes instead of mocks.
class UsingFakesWithDependencyInjection(SimpleTestCase):

    def test_no_mocking_(self):
        # setup
        fake_billing_system = FakeBillingSystem()
        fake_formatter = FakeFormatter()

        # Pass the dependencies via the constructor.
        formatter = PayPerUseStringFormatter(
            formatter=fake_formatter,
            billing_system=fake_billing_system
        )

        # execute
        new_balance, concatenated_result = formatter.concatenate('string1', 'string2', 'string3')

        # assert
        # not having a direct reference to the mock makes calling assert methods awkward though.
        self.assertEqual(50, new_balance)
        self.assertEqual(AccountDebit('AC123', 100), fake_billing_system._debit)
        self.assertEqual('string1 string2 string3', concatenated_result)


# If you prefer fakes to mocks, but don't have "seams" through which to inject them, then you can fall back to
# using patch to replace the actual implementations.
class UsingFakesWithPatch(SimpleTestCase):

    # patch is kind of gross, and with a few minor changes can help you completely avoid it.
    # the target classes/callables are replace with the value of 'new'
    # mocks are no longer passed as params to the test method.
    @patch('testapp.billing.BillingSystem', new=FakeBillingSystem)
    @patch('testapp.pay_per_use_formatter.SlowStringFormatter', new=FakeFormatter)
    def test_patching_classes(self):
        # setup
        # Pass the dependencies via the constructor.
        formatter = PayPerUseStringFormatter()

        # execute
        new_balance, concatenated_result = formatter.concatenate('string1', 'string2', 'string3')

        # assert
        # not having a direct reference to the mock makes calling assert methods awkward though.
        self.assertEqual(50, new_balance)
        # This obviously wouldn't work if we weren't saving a reference on the instance.
        self.assertEqual(AccountDebit('AC123', 100), formatter.billing_system._debit)
        self.assertEqual('string1 string2 string3', concatenated_result)