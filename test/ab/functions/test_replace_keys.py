import inspect
import pytest

import random
from test.common.primitives import random_word, random_value
from test.common.test import create

from tasks.ab.functions import replace_keys


class TestReplaceKeys:
    @staticmethod
    def _gen(common, replace):
        c = [random_word(10) for _ in range(common)]
        r = [(random_word(10), random_word(10)) for _ in range(replace)]
        d1, d2 = {}, {}
        for w in r + list(zip(c, c)):
            v = random_value(10)
            d1[w[0]] = v
            d2[w[1]] = v
        return [d1], dict(r), d2

    @staticmethod
    def _gen_chain(size):
        w1 = [random_word(10) for _ in range(size)]
        w2 = w1[1:] + [w1[0]]
        d1, d2 = {}, {}
        for w in zip(w1, w2):
            v = random_value(10)
            d1[w[0]] = v
            d2[w[1]] = v
        return [d1], dict(zip(w1, w2)), d2

    def test_all(self):
        runner = create(replace_keys, 'test_all', self._gen)
        runner.multitest(
            runner.manual({'x': 1, 'y': 2}, x='z').returns({'z': 1, 'y': 2}),
            runner.manual({'x': 1, 'y': 2, 'z': 3}, x='y', y='z', z='x', p='q').returns({'y': 1, 'z': 2, 'x': 3}),

            runner.auto(4, 0),
            runner.auto(4, 2),
            runner.auto(2, 10),
            runner.auto(1000, 1000),

            runner.auto(2, gen=self._gen_chain),
            runner.auto(5, gen=self._gen_chain),
            runner.auto(10, gen=self._gen_chain)
        )
