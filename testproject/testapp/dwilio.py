
class BestSellerNotification(object):

    def __init__(self, book):
        self.book = book

    def message(self):
        return f'Congratulations {self.book.author.name}, your book {self.book.title} sold {self.book.total_sold} ${self.book.total_sales} this week'

    def to_number(self):
        return self.book.author.phone_number


class DwilioClient(object):

    def _send_to_api(self):
        pass

    def send_notification(self, notification):
        self._send_to_api(notification.to_number, notification.message)
