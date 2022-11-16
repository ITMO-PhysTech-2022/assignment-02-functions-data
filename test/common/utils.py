import pytest
from threading import Thread, Event


def _singleton(cls):
    instance = None

    def create(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return create


def identity(data):
    return data


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

    # _run.__name__ = spec.__name__
    return _run


def feedback_and_fail(data, answer, msg):
    with open('test.log', 'w', encoding='utf-8') as f:
        print(f'Входные данные:\n{data}', file=f)
        print(f'Ожидаемый ответ:\n{answer}', file=f)
        print(f'Вердикт:\n{msg}', file=f)
    pytest.fail(msg)


def equality(result, answer):
    if result == answer:
        return True, 'Ok'
    return False, 'Not equal'


def multitest(gen, check, spec, tests):
    for i, test in enumerate(tests):
        data, answer = gen(**test)
        try:
            verdict, msg = check(spec(*data), answer)
            if not verdict:
                feedback_and_fail(data, answer,
                                  f'Неверный ответ на тесте {i + 1}: {msg}')
        except TimeoutError:
            feedback_and_fail(data, answer,
                              f'Превышено ограничение времени на тесте {i + 1}')
