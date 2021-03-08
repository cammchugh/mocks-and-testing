from dataclasses import dataclass


class BillingSystemException(Exception):
    pass


@dataclass(frozen=True)
class AccountDebit:
    account_id: str
    amount: int


class BillingSystem(object):

    def charge_for_usage(self, debit: AccountDebit):

        # this would talk to a real billing system.
        def _call_billing_api(url, post_body):
            # return {
            #     'status_code': 200,
            #     'response': { 'success': True, 'new_balance': 50}
            # }
            raise Exception('No billing allowed during tests')

        post_body = {
            'account_id': debit.account_id,
            'amount': debit.amount
        }

        return _call_billing_api('http://example.com/billing', post_body)








