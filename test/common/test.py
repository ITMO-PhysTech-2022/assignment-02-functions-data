import os
import re
import shutil
import pathlib

import pytest
import re

from copy import deepcopy
from threading import Thread, Event


def _singleton(cls):
    instance = None

    def create(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return create


def _root_directory():
    path = pathlib.Path().absolute()
    candidates = [path] + list(path.parents)
    for parent in candidates:
        if parent.parts[-1].startswith('assignment'):
            return parent
    raise AssertionError('Expected to find the assignment root as a parent directory')


def _trim_message(msg):
    lines = msg.split('\n')
    first_line = 0
    while first_line < len(lines) and lines[first_line].strip() == '':
        first_line += 1
    lines = lines[first_line:]

    max_prefix = max([len(re.match(r'^\s*', line).group()) for line in lines])
    return '\n'.join([line[max_prefix:] for line in lines])


class TestInstantiationError(Exception):
    pass


class _TestBase:
    _root_path = _root_directory() / 'testlog'

    @staticmethod
    def _default_check(result, answer):
        if result != answer:
            return False, 'Ответ отличается от ожидаемого'
        return True, 'Ok'

    def __init__(self, spec, test_name, gen=None, check=None):
        self.spec = spec
        self.test_name = test_name

        self.default_gen = gen
        self.check = _TestBase._default_check if check is None else check

        self.path = _TestBase._root_path.joinpath(self.spec.__name__)
        self.path.mkdir(parents=True, exist_ok=True)
        self.path /= (self.test_name + '.log')
        if self.path.exists():
            os.remove(self.path)

    class _Test:
        def __init__(self, args, kwargs, answer):
            self.args = args
            self.kwargs = kwargs
            self.answer = answer

    class _Handler:
        def __init__(self, args, kwargs):
            self._args = args
            self._kwargs = kwargs

        def returns(self, return_value):
            return _TestBase._Test(self._args, self._kwargs, return_value)

    @staticmethod
    def manual(*args, **kwargs):
        return _TestBase._Handler(args, kwargs)

    def auto(self, *args, **kwargs):
        gen = kwargs.pop('gen', self.default_gen)
        data = gen(*args, **kwargs)
        if len(data) == 2:
            test_args, test_answer = data
            test_kwargs = {}
        else:
            test_args, test_kwargs, test_answer = data
        return _TestBase._Test(test_args, test_kwargs, test_answer)

    def multitest(self, *tests):
        for test_no, test in enumerate(tests):
            try:
                args_c, kwargs_c = deepcopy(test.args), deepcopy(test.kwargs)
                result = self.spec(*args_c, **kwargs_c)
                verdict, msg = self.check(result, test.answer)
                if not verdict:
                    self.report_wa(test_no + 1, test, result, msg)
                    pytest.fail(f'Неверный ответ на тесте {self.test_name}/{test_no + 1}:\n{msg}')
            except TimeoutError:
                self.report_tl(test_no + 1, test)
                pytest.fail(f'Превышено время работы на тесте {self.test_name}/{test_no + 1}')
            except Exception as e:
                self.report_re(test_no + 1, test, e)
                raise e

    def report_wa(self, test_no, test, result, msg):
        with open(self.path, 'a', encoding='utf-8') as log:
            log.write(_trim_message(f'''
            ========================================
            Неверный ответ на тесте {test_no}
            {msg}
            
            Входные данные:
            - args      : {test.args}
            - kwargs    : {test.kwargs}
            
            Результат:
            - ожидалось : {test.answer}
            - получено  : {result}
            \n'''))

    def report_tl(self, test_no, test):
        with open(self.path, 'a', encoding='utf-8') as log:
            log.write(_trim_message(f'''
            ========================================
            Превышено время работы на тесте {test_no}

            Входные данные:
            - args      : {test.args}
            - kwargs    : {test.kwargs}
            \n'''))

    def report_re(self, test_no, test, ex):
        with open(self.path, 'a', encoding='utf-8') as log:
            log.write(_trim_message(f'''
            ========================================
            Ошибка в работе решения на тесте {test_no}
            {repr(ex)}

            Входные данные:
            - args      : {test.args}
            - kwargs    : {test.kwargs}
            \n'''))


create = _TestBase


def timeout(spec, seconds=5.0):
    result = None

    def _worker(*args, **kwargs):
        nonlocal result
        result = spec(*args, **kwargs)

    def _run(*args, **kwargs):
        thread = Thread(target=_worker, args=args, kwargs=kwargs)
        thread._stop_event = Event()
        try:
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                raise TimeoutError('Function took too long to execute')
            return result
        finally:
            thread._stop_event.set()

    _run.__name__ = spec.__name__
    return _run
