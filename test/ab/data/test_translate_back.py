import inspect
import pytest

import random
from test.common.primitives import random_word
from test.common.test import create

from tasks.ab.data import translate_back


class TestTranslateBack:
    @staticmethod
    def _gen(n, m):
        lang1 = [random_word(10) for _ in range(n)]
        lang2 = [random_word(10) for _ in range(n)]
        d1, d2 = {}, {}
        for _ in range(m):
            w1, w2 = random.choice(lang1), random.choice(lang2)
            if w1 not in d1: d1[w1] = []
            if w2 not in d2: d2[w2] = []
            d1[w1].append(w2)
            d2[w2].append(w1)
        return [d1], d2

    @staticmethod
    def spawn(test_name):
        return create(translate_back, test_name, TestTranslateBack._gen)

    def test_all(self):
        runner = self.spawn('test_all')
        runner.multitest(
            runner.manual({
                'apple': ['malum', 'pomum', 'popula'],
                'fruit': ['popum'],
                'punishment': ['malum', 'multa']
            }).returns({
                'malum': ['apple', 'punishment'],
                'pomum': ['apple'],
                'popula': ['apple'],
                'popum': ['fruit'],
                'multa': ['punishment']
            }),

            runner.auto(2, 3),
            runner.auto(5, 10),
            runner.auto(50, 1000),
            runner.auto(700, 100000)
        )
