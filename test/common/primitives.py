import random


def random_word(length: int, chars=None) -> str:
    if chars is None:
        chars = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    word = ''.join(random.choices(chars, k=length))
    return word


def random_value(size: int):
    randint = lambda: random.randint(-size, size)
    options = [
        randint,
        lambda: random.random() * size,
        lambda: [randint() for _ in range(abs(randint()))],
        lambda: random_word(size)
    ]
    return random.choice(options)()