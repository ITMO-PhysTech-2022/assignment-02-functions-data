import inspect
import pytest

import random
from test.common.test import create

from tasks.ab.functions import generate_json


class TestGenerateJson:
    @staticmethod
    def _gen(n):
        return [n], n

    @staticmethod
    def _check(result, answer):
        if not isinstance(result, dict):
            return False, f'Ожидалось, что функция вернет словарь'
        keys = 3

        def _depth(obj):
            d = 1
            nonlocal keys
            keys = min(keys, len(obj))
            for k, v in obj.items():
                if isinstance(v, dict):
                    d = max(d, _depth(v) + 1)
            return d

        depth = _depth(result)
        if keys < 3:
            return False, f'Минимальное количество ключей в словарях равно {keys}, а должно быть не меньше 3'
        if depth != answer:
            return False, f'Уровень вложенности равен {depth}, а должен быть равен {answer}'
        return True, 'Ok'

    def test_all(self):
        runner = create(generate_json, 'test_all', self._gen, self._check)
        runner.multitest(
            runner.auto(1),
            runner.auto(2),
            runner.auto(3),
            runner.auto(10),
            runner.auto(47),
            runner.auto(100)
        )