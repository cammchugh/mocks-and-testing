from time import sleep


class SlowStringFormatter(object):

    def really_slow_string_format(self, string1, string2):
        self._this_is_the_slow_part()
        return f'{string1} {string2}'

    def _this_is_the_slow_part(self):
        sleep(10)