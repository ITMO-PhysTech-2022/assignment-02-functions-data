import inspect
import pytest

import random
from test.common.test import create
from test.common.mockit import mock_print

from tasks.ab.functions import print_tree


class TestPrintTree:
    @staticmethod
    def _spec(*args, **kwargs):
        with mock_print() as output:
            print_tree(*args, **kwargs)
            return output.getvalue()

    @staticmethod
    def _gen(n):
        return [n], n

    @staticmethod
    def _check(result, answer):
        n = answer
        result = result.split('\n')
        while len(result) > 0 and result[-1].strip() == '':
            result.pop()
        if len(result) != n * (n + 1) // 2:
            return False, f'Ожидалось {n * (n + 1) // 2} строк в выводе, выведено {len(result)}'

        idx = 0
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                s = j * 2 - 1
                spaces, stars, stage = 0, 0, 0
                for c in result[idx]:
                    if stage == 0:
                        if c == ' ':
                            spaces += 1
                        else:
                            stage = 1
                    if stage == 1:
                        if c == '*':
                            stars += 1
                        else:
                            stage = 2
                    if stage == 2:
                        if c != ' ':
                            return False, f'На строке {idx + 1} встречен символ \'{c}\' после полосы из \'*\''
                if spaces != n - j:
                    return False, f'Ожидалось {n - j} пробелов в начале {idx + 1}-й строки, выведено {spaces}'
                if stars != s:
                    return False, f'Ожидалась полоса из {s} звезд на строке {idx + 1}, выведено {stars}'
                idx += 1

        return True, 'Ok'

    def test_all(self):
        self._spec.__name__ = print_tree.__name__
        runner = create(self._spec, 'test_all', self._gen, self._check)
        runner.multitest(
            runner.auto(1),
            runner.auto(2),
            runner.auto(3),
            runner.auto(5),
            runner.auto(10),
            runner.auto(47),
            runner.auto(100)
        )
