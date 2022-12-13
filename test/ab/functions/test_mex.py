import inspect
import re

import pytest

import random
from test.common.test import create

from tasks.ab.functions import mex


class TestMex:
    @staticmethod
    def _gen(n, result):
        data = list(range(n))
        data.pop(data.index(result))
        random.shuffle(data)
        return data, result

    def test_all(self):
        runner = create(mex, 'test_all', self._gen)
        runner.multitest(
            runner.manual(1, 5, 3, 0, 2, 6).returns(4),
            runner.manual(1, 2, 3, 4).returns(0),
            runner.manual().returns(0),
            runner.manual(0, 7, 2, 5, 8, 1, 4, 3).returns(6),

            runner.auto(100, 42),
            runner.auto(1234, 1233),
            runner.auto(10000, 0),
            runner.auto(10000, 1),
            runner.auto(10000, 199),
            runner.auto(10000, 4747)
        )
