import inspect
import pytest

import random
from test.common.test import create

from tasks.ab.data import extract_each


class TestExtractEach:
    @staticmethod
    def _gen_basic(k):
        data = random.choices(range(1000), k=k - 1)
        args = [data * k, k]
        return args, {'cyclic': False}, data

    @staticmethod
    def _gen_cyclic(k):
        data = random.choices(range(1000), k=k - 1)
        args = [data * k, k + 1]
        answer = data[::2] if k % 2 == 1 else data[::2] + data[1::2]
        return args, {'cyclic': True}, answer * k

    @staticmethod
    def spawn(test_name, **kwargs):
        return create(extract_each, test_name, **kwargs)

    def test_basic(self):
        runner = self.spawn('test_basic', gen=self._gen_basic)
        runner.multitest(
            runner.manual([1, 2, 3, 4], 1).returns([1, 2, 3, 4]),
            runner.manual([1, 2, 3, 4, 5], 2).returns([1, 3, 5]),
            runner.manual([1, 2, 3, 4], 3).returns([1, 4]),
            runner.manual(list(range(1000)), 17).returns(list(range(0, 1000, 17))),

            runner.auto(2),
            runner.auto(3),
            runner.auto(4),
            runner.auto(5),
            runner.auto(17)
        )

    def test_cyclic(self):
        runner = self.spawn('test_cyclic', gen=self._gen_cyclic)
        runner.multitest(
            runner.manual([], 2, cyclic=True).returns([]),
            runner.manual([1, 2, 3, 4], 3, cyclic=True).returns([1, 4, 3, 2]),
            runner.manual([1, 2, 3, 4, 5, 6], 3, cyclic=True).returns([1, 4]),
            runner.manual([1, 2, 3, 4, 5, 6, 7], 4, cyclic=True).returns([1, 5, 2, 6, 3, 7, 4]),

            runner.auto(2),
            runner.auto(3),
            runner.auto(4),
            runner.auto(5),
            runner.auto(17)
        )
