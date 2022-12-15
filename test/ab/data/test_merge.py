import inspect
import pytest

import random
from copy import deepcopy
from test.common.primitives import random_word, random_value
from test.common.test import create

from tasks.ab.data import merge


class TestMerge:
    @staticmethod
    def _gen_basic(common, left, right):
        keys = [random_word(10) for _ in range(common + left + right)]
        random.shuffle(keys)
        m, l, r = keys[:common], keys[common:common + left], keys[-right:]
        d1, d2, d3 = {k: random_value(7) for k in m}, {}, {}
        for d, k in ((d1, m), (d2, l), (d3, r)):
            d.update({key: random_value(7) for key in k})

        r1, r2, r3 = deepcopy(d1), deepcopy(d3), deepcopy(d3)
        r1.update(d2)
        r2.update(d1)
        r3.update(d1)
        r3.update(d2)
        return [r1, r2], r3

    @staticmethod
    def _gen_recursive(depth, width, spam=1):
        dd, dd_ans = TestMerge._gen_basic(spam, spam, spam)
        for i in range(depth):
            par, par_ans = TestMerge._gen_basic(width, spam, spam)
            sib, sib_ans = TestMerge._gen_basic(width // 2, width, width)
            w1, w2 = random_word(6), random_word(6)
            par[0][w1], par[1][w1], par_ans[w1] = dd[0], dd[1], dd_ans
            par[0][w2], par[1][w2], par_ans[w2] = sib[0], sib[1], sib_ans

            bs, _ = TestMerge._gen_basic(width // 2, width // 2, width // 2)
            w3, w4, rv_ans = random_word(5), random_word(5), random_value(width)
            par[0][w3], par[1][w3], par_ans[w3] = bs[0], random_value(width), bs[0]
            par[0][w4], par[1][w4], par_ans[w4] = rv_ans, bs[1], rv_ans

            dd, dd_ans = par, par_ans
        return dd, {'recursive': True}, dd_ans

    @staticmethod
    def spawn(test_name, **kwargs):
        return create(merge, test_name, **kwargs)

    def test_basic(self):
        runner = self.spawn('test_basic', gen=self._gen_basic)
        runner.multitest(
            runner.manual({'x': 10}, {'y': 20}).returns({'x': 10, 'y': 20}),
            runner.manual({'x': 20}, {'x': 30}).returns({'x': 20}),
            runner.manual({'x': {'y': 20}}, {'x': {'z': 30}}).returns({'x': {'y': 20}}),

            runner.auto(0, 10, 15),
            runner.auto(0, 15, 10),
            runner.auto(10, 10, 10),
            runner.auto(100, 100, 100)
        )

    def test_recursive(self):
        runner = self.spawn('test_recursive', gen=self._gen_recursive)
        runner.multitest(
            runner.manual({'x': {'y': 20}}, {'x': {'z': 30}}, True).returns({'x': {'y': 20, 'z': 30}}),
            runner.manual({
                'name': {'second': 'Oreshnikov'},
                'age': 23,
                'tmp': {
                    'records': {
                        '02/12/1999': 'can\'t remember',
                        '18/11/2022': '<3'
                    },
                    'who': 'Yes',
                    'yes': ['what', 'is' 'this'],
                    'no': {'yes': 'no'},
                    'x': {'y': {'z': 10}}
                }
            }, {
                'name': {'first': 'Dan', 'second': '???'},
                'age': 20,
                'tmp': {
                    'records': {
                        '02/12/1999': 'wow',
                        '01/01/2006': 'wtf'
                    },
                    'who': {
                        'what': '?',
                        'yes': 'no'
                    },
                    'yes': ['no'],
                    'no': 'my imagination has already ran out',
                    'x': {'y': {'Z': 100}}
                }
            }, True).returns({
                'name': {'first': 'Dan', 'second': 'Oreshnikov'},
                'age': 23,
                'tmp': {
                    'records': {
                        '02/12/1999': 'can\'t remember',
                        '18/11/2022': '<3',
                        '01/01/2006': 'wtf'
                    },
                    'who': 'Yes',
                    'yes': ['what', 'is' 'this'],
                    'no': {'yes': 'no'},
                    'x': {'y': {'z': 10, 'Z': 100}}
                }
            }),

            runner.auto(1, 2),
            runner.auto(2, 3),
            runner.auto(5, 5),
            runner.auto(10, 2),
            runner.auto(20, 100)
        )
