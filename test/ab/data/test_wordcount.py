import inspect
import pytest

import random
from test.common.primitives import random_word
from test.common.test import create, timeout

from tasks.ab.data import wordcount


class TestWordcount:
    @staticmethod
    def _gen(length, dif, count, case=False, signs=False):
        if isinstance(length, int):
            length = [length]
        words, answer = [], {}
        for i in range(dif):
            word = random_word(random.choice(length))
            cnt = max(1, random.randint(count // 2, count))
            batch = [word] * cnt
            if case:
                for idx in range(len(batch)):
                    item = list(batch[idx])
                    pos = random.randint(0, len(item) - 1)
                    item[pos] = item[pos].upper()
                    batch[idx] = ''.join(item)
            words += [word] * cnt
            answer[word] = answer.get(word, 0) + cnt
        random.shuffle(words)
        if signs:
            options = [',', ':', '.', '!']
            for idx in range(len(words) - 1):
                words[idx] += random.choice(options)
        return [' '.join(words)], answer

    @staticmethod
    def _check(result, answer):
        if not isinstance(result, dict):
            return False, f'Ожидалось, что функция вернет словарь'
        if len(result) != len(answer):
            return False, f'Ожидалось {len(answer)} различных слов, найдено {len(result)}'
        used = set()
        for key, value in result.items():
            word = key.lower()
            if word not in answer or word in used:
                return False, f'Лишнее слово \'{key}\''
            if value != answer[word]:
                return False, f'Ожидалось {answer[word]} вхождений слова \'{word}\', найдено {value}'
            used.add(word)
        return True, 'Ok'

    @staticmethod
    def spawn(test_name):
        return create(wordcount, test_name, TestWordcount._gen, TestWordcount._check)

    def test_basic(self):
        runner = self.spawn('test_basic')
        runner.multitest(
            runner.manual('word').returns({'word': 1}),
            runner.manual('two words').returns({'two': 1, 'words': 1}),
            runner.manual('one two and two ones').returns({'one': 1, 'two': 2, 'and': 1, 'ones': 1}),
            runner.manual('a sub word and subword').returns({'a': 1, 'sub': 1, 'word': 1, 'and': 1, 'subword': 1}),
            runner.manual('abc abc abd abc').returns({'abc': 3, 'abd': 1}),
            runner.manual('').returns({}),

            runner.auto(length=[1, 2], dif=10, count=10),
            runner.auto(length=[1, 5, 10], dif=10, count=10),
            runner.auto(length=100, dif=10, count=10),
            runner.auto(length=100, dif=1, count=100),
            runner.auto(length=100, dif=100, count=1)
        )

    def test_noise(self):
        runner = self.spawn('test_noise')
        runner.multitest(
            runner.auto(length=[1, 2], dif=10, count=10, case=True),
            runner.auto(length=[1, 5, 10], dif=10, count=10, signs=True),
            runner.auto(length=[1, 100], dif=10, count=10, case=True, signs=True),
            runner.auto(length=100, dif=1, count=100, case=True, signs=True),
            runner.auto(length=100, dif=100, count=1, case=True, signs=True),
        )

    def test_large(self):
        runner = create(timeout(wordcount), 'test_large', self._gen, self._check)
        runner.multitest(
            runner.auto(length=100, dif=1000, count=100),
            runner.auto(length=10, dif=100, count=1000),
            runner.auto(length=10, dif=10000, count=10),
            runner.auto(length=1, dif=50000, count=20),
            runner.auto(length=1, dif=200, count=5000),
            runner.auto(length=5, dif=1000, count=1000)
        )
