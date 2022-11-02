def pytest_addoption(parser):
    parser.addoption(
        '--line',
        action='store',
        default=None,
        help='Output lines to check or None for \'everything\''
    )


def pytest_generate_tests(metafunc):
    if 'line' not in metafunc.fixturenames:
        return
    line = metafunc.config.getoption('line')
    if line is not None:
        line = int(line) - 1
    metafunc.parametrize('line', [line])
