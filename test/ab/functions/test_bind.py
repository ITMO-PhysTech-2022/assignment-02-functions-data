import inspect
import re

import pytest

import random
from test.common.test import create

from tasks.ab.functions import bind


class TestBind:
    @staticmethod
    def _check(result, answer):
        f, tests = answer
        for test in tests:
            a = f(*test)
            try:
                r = result(*test)
            except (BaseException, Exception) as e:
                return False, f'Возвращаемая функция вызывает ошибку при запуске на {test}: {e}'
            if r != a:
                return False, f'Ожидалось значение {a} на тесте {test}, получено {r}'
        return True, 'Ok'

    @staticmethod
    def _wrap(tests):
        return [[test] for test in tests]

    def test_all(self):
        tests = self._wrap(range(-20, 21))
        runner = create(bind, 'test_all', check=self._check)
        runner.multitest(
            runner.manual(lambda x, y: x - y, _1=10).returns(
                (lambda y: 10 - y, tests)
            ),
            runner.manual(lambda x, y: x - y, _2=10).returns(
                (lambda x: x - 10, tests)
            ),
            runner.manual(lambda x, y, z: x * y + z, _1=1, _3=2).returns(
                (lambda y: y + 2, tests)
            ),
            runner.manual(lambda x, y, z: x * y + z, _1=2, _2=3).returns(
                (lambda z: z + 6, tests)
            ),
            runner.manual(lambda x, y, z: x * y + z, _2=3, _3=4).returns(
                (lambda x: 3 * x + 4, tests)
            ),
            runner.manual(lambda x, y, z: x * y + z, _1=3, _2=4, _3=5).returns(
                (lambda: 17, [[]])
            ),
            runner.manual(lambda x, y, z, a, b, c: x * a + y * b + z * c, _1=-1, _5=-2, _3=3, _6=4).returns(
                (lambda y, a: -a - 2 * y + 12, list(zip(range(-20, 21), range(20, -21, -1))))
            )
        )
