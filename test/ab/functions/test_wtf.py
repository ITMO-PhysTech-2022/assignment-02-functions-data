import inspect
import re

import pytest

import random
from test.common.test import create

from tasks.ab.functions import wtf

# please ignore the fact that this is an awful way to check function's structure
source = re.escape('''def wtf():
    """
    Функция wtf вызывает внутреннюю функцию _worker с некоторым аргументом
    и должна возвращать число 42
    """

    def _worker(x):
        if x == 0:
            return wtf()
        elif x % 2 == 1:
            return _worker(x // 3) + 1
        elif x % 982 == 0:
            return _worker(x + 982 if x < 10000 else x - 2) + 1
        else:
            return 0

    return _worker(''') + r'(\d*|\.\.\.)' + re.escape(''')
''')


class TestWtf:
    def test_all(self):
        src = inspect.getsource(wtf)
        if not re.fullmatch(source, src):
            pytest.fail('Функция была изменена больше, чем было разрешено по заданию')

        try:
            result = wtf()
        except (BaseException, Exception) as e:
            pytest.fail(f'Функция вызывает ошибку: {e}')
        if result != 42:
            pytest.fail(f'Функция должна возвращать 42, а возвращает {result}')
