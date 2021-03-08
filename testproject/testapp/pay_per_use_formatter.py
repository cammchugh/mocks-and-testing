import testapp.billing
from testapp.slow_formatter import SlowStringFormatter


class PayPerUseStringFormatter(object):

    # region __init__
    def __init__(self, formatter=None, billing_system=None):
        self.billing_system = billing_system or testapp.billing.BillingSystem()
        self.formatter = formatter or SlowStringFormatter()
    # endregion

    def concatenate(self, string1, string2, string3):
        account_debit = testapp.billing.AccountDebit('AC123', 100)
        result = self.billing_system.charge_for_usage(account_debit)
        if result['status_code'] == 200:
            slow_string = self.formatter.really_slow_string_format(string1, string2)
            new_balance = result['response']['new_balance']
            return new_balance, f'{slow_string} {string3}'
        else:
            raise testapp.billing.BillingSystemException()
