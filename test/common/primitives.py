import random


def random_word(length: int, chars=None) -> str:
    if chars is None:
        chars = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    word = ''.join(random.choices(chars, k=length))
    return word