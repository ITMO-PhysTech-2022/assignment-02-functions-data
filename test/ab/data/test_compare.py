import inspect
import pytest

import random
from test.common.test import create

from tasks.ab.data import compare


class TestCompare:
    @staticmethod
    def _gen(common, left, right):
        a = list(range(common + left + right))
        random.shuffle(a)
        m, l, r = a[:common], a[common:common + left], a[-right:]
        return [set(m + l), set(m + r)], min(l, default=-1) < min(r, default=-1)

    def test_all(self):
        runner = create(compare, 'test_all', self._gen)
        runner.multitest(
            runner.manual({1, 2, 3}, {1, 2, 3}).returns(False),
            runner.manual({1, 2}, {1, 2, 3}).returns(True),
            runner.manual({1, 2, 4}, {1, 2, 5}).returns(True),
            runner.manual({4, 3, 2, 1}, {4, 3, 2, 0}).returns(False),
            runner.manual({4, 3, 2, 1}, {4, 3, 2, 1, 0}).returns(True),

            runner.auto(0, 0, 2),
            runner.auto(0, 2, 0),
            runner.auto(1000, 0, 1000),
            runner.auto(1000, 1000, 1000),
            runner.auto(1000, 1000, 100),
            runner.auto(1000, 1000, 10)
        )
