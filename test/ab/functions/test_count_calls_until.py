import inspect
import re

import pytest

import random
from test.common.test import create

from tasks.ab.functions import count_calls_until


class TestCountCallsUntil:
    def test_all(self):
        cnt = 0

        def _helper1(x):
            nonlocal cnt
            cnt += 1
            return x

        def _helper2(x):
            x.append(len(x))
            return x

        runner = create(count_calls_until, 'test_all')
        runner.multitest(
            runner.manual(lambda x: x + 2, 0, lambda x: x > 10).returns(6),
            runner.manual(lambda x: x // 10, 1257513, lambda x: x == 0).returns(7),
            runner.manual(lambda x: x + x, 'a', lambda x: len(x) > 1000).returns(10),
            runner.manual(_helper1, 0, lambda x: cnt > 10).returns(11),
            runner.manual(_helper2, [], lambda x: sum(x) > 10000).returns(142),
            runner.manual(lambda x: None, 10, lambda x: x is None).returns(1),
            runner.manual(lambda x: None, None, lambda x: x is None).returns(0)
        )
