import inspect
import pytest

import random
from test.common.primitives import random_word
from test.common.utils import identity, equality, timeout, multitest

import tasks.ab.data


class TestWordcount:
    spec = tasks.ab.data.wordcount

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

    def test_basic(self):
        multitest(identity, TestWordcount._check, TestWordcount.spec, [
            {'data': (['word'], {'word': 1})},
            {'data': (['two words'], {'two': 1, 'words': 1})},
            {'data': (['one two and two ones'], {'one': 1, 'two': 2, 'and': 1, 'ones': 1})},
            {'data': (['a sub word and subword'], {'a': 1, 'sub': 1, 'word': 1, 'and': 1, 'subword': 1})},
            {'data': (['abc abc abd abc'], {'abc': 3, 'abd': 1})},
            {'data': ([''], {})}
        ])
        multitest(TestWordcount._gen, TestWordcount._check, TestWordcount.spec, [
            {'length': [1, 2], 'dif': 10, 'count': 10},
            {'length': [1, 5, 10], 'dif': 10, 'count': 10},
            {'length': 100, 'dif': 10, 'count': 10},
            {'length': 100, 'dif': 1, 'count': 100},
            {'length': 100, 'dif': 100, 'count': 1}
        ])

    def test_advanced(self):
        multitest(TestWordcount._gen, TestWordcount._check, TestWordcount.spec, [
            {'length': [1, 2], 'dif': 10, 'count': 10, 'case': True},
            {'length': [1, 5, 10], 'dif': 10, 'count': 10, 'signs': True},
            {'length': [1, 100], 'dif': 10, 'count': 10, 'case': True, 'signs': True},
            {'length': 100, 'dif': 1, 'count': 100, 'case': True, 'signs': True},
            {'length': 100, 'dif': 100, 'count': 1, 'case': True, 'signs': True}
        ])

    def test_large(self):
        spec = timeout(TestWordcount.spec, 1.0)
        multitest(TestWordcount._gen, TestWordcount._check, spec, [
            {'length': 100, 'dif': 1000, 'count': 100},
            {'length': 10, 'dif': 100, 'count': 1000},
            {'length': 10, 'dif': 10000, 'count': 10, 'case': True},
            {'length': 1, 'dif': 50000, 'count': 20, 'signs': True},
            {'length': 1, 'dif': 200, 'count': 5000, 'case': True, 'signs': True}
        ])
