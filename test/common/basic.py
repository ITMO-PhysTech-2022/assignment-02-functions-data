import pytest


def check_printable(answers, results, line):
    def _test_step(step):
        if len(answers) <= step:
            pytest.fail(f'Пункт {step + 1} не существует')
        if len(results) <= step:
            pytest.fail(f'Ожидалось хотя бы {step + 1} строк в выводе, выведено {len(results)}')
        if str(answers[step]) != results[step]:
            pytest.fail(f'Выведен неверный результат на шаге {step + 1}: '
                        f'\n\t>ожидалось {answers[step]}'
                        f'\n\t>выведено  {results[step]}')

    lines = [line]
    if line is None:
        lines = list(range(len(answers)))
    for line in lines:
        _test_step(line)
