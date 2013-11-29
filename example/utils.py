# Test utils for the example app.
import datetime
import mock
from functools import wraps

class Today(object):
    """Class used to mock out the datetime.date.

    https://code.djangoproject.com/ticket/21523#comment:10
    """ 
    def __init__(self, *args):
        mocked_today = datetime.date(*args)
        self.mocked_date_cls = type(
            'mocked_date_cls',
            (datetime.date,),
            {'today': staticmethod(lambda: mocked_today)}
        )

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with mock.patch('datetime.date', self.mocked_date_cls):
                return func(*args, **kwargs)
        return wrapper


class FakeDate(datetime.date):
    """Alternative mocking solution.

    https://code.djangoproject.com/ticket/21523#comment:9
    """
    @classmethod
    def today(cls):
        return cls(2000, 1, 1)