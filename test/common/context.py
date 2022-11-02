import random


def get_integer():
    return random.randint(1, 1000)


def get_float():
    return random.random()


def get_string():
    alpha = list(range(ord('a'), ord('z') + 1))
    letters = random.choices(alpha, k=30)
    return ''.join(map(chr, letters))


def useless_function():
    pass
