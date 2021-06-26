from unittest.mock import call, Mock

from rabbitai.utils import decorators
from tests.base_tests import RabbitaiTestCase


class UtilsDecoratorsTests(RabbitaiTestCase):
    def test_debounce(self):
        mock = Mock()

        @decorators.debounce()
        def myfunc(arg1: int, arg2: int, kwarg1: str = "abc", kwarg2: int = 2):
            mock(arg1, kwarg1)
            return arg1 + arg2 + kwarg2

        # should be called only once when arguments don't change
        myfunc(1, 1)
        myfunc(1, 1)
        result = myfunc(1, 1)
        mock.assert_called_once_with(1, "abc")
        self.assertEqual(result, 4)

        # kwarg order shouldn't matter
        myfunc(1, 0, kwarg2=2, kwarg1="haha")
        result = myfunc(1, 0, kwarg1="haha", kwarg2=2)
        mock.assert_has_calls([call(1, "abc"), call(1, "haha")])
        self.assertEqual(result, 3)
