import inspect
import re

import pytest

import random
from test.common.primitives import random_word, random_value
from test.common.mockit import mock_print
from test.common.test import create

from tasks.ab.functions import useless_function


class TestUselessFunction:
    def test_all(self):
        src = inspect.getsource(useless_function)
        expected_src = '''
            print('What is happening?...')
            print('Why is it happening?...')
            if True is False:
                exit(1)  # beautiful death
            return UserWarning
        '''
        for comment in ["'''", '"""']:
            pattern = fr'{comment}[^{comment[0]}]{comment}'
            src = re.sub(pattern, '', src)
        src = re.sub(r'(^|\n)#[^\n]*\n?', '', src)

        for line in expected_src.split('\n'):
            line = line.strip()
            if line not in src:
                pytest.fail(f'Ожидалось увидеть строчку \'{line}\' в коде функции')

        with mock_print() as output:
            try:
                result = useless_function()
                output_value = output.getvalue()
            except (BaseException, Exception) as e:
                pytest.fail(f'Функция вызывает ошибку: {e}')
        if result is not None:
            pytest.fail(f'Ожидалось, что функция ничего не вернет, но функция вернула {result}')
        if output_value != '':
            pytest.fail(f'Ожидалось, что функция ничего не напечатает')
