import inspect
import re

import pytest

import random
from test.common.primitives import random_word
from test.common.test import create

from tasks.ab.data import caesar_encode, caesar_decode


class TestCaesarEncode:
    @staticmethod
    def spawn(test_name):
        return create(caesar_encode, test_name)

    def test_basic(self):
        runner = self.spawn('test_basic')
        runner.multitest(
            runner.manual('simple identity', 26).returns('simple identity'),
            runner.manual('caesar', 1).returns('bzdrzq'),
            runner.manual('', 21).returns(''),
            runner.manual('some random text', 19).returns('zvtl yhukvt alea'),
            runner.manual('the quick brown fox jumps over the lazy dog', 9).returns(
                'kyv hlztb sifne wfo aldgj fmvi kyv crqp ufx'),
            runner.manual('abcdefghijklmnopqrstuvwxyz', 23).returns('defghijklmnopqrstuvwxyzabc'),
        )

    def test_cases(self):
        runner = self.spawn('test_cases')
        runner.multitest(
            runner.manual('Simple Identity', 26).returns('Simple Identity'),
            runner.manual('Encode this', 11).returns('Tcrdst iwxh'),
            runner.manual('Please Do Not Ignore Upper Case', 14).returns('Bxqmeq Pa Zaf Uszadq Gbbqd Omeq'),
            runner.manual('CAPS LOCK IS ON', 8).returns('USHK DGUC AK GF'),
            runner.manual('WhY aM I sPeNdInG tImE oN tHiS', 8).returns('OzQ sE A kHwFvAfY lAeW gF lZaK')
        )


class TestCaesarDecode:
    @staticmethod
    def _gen(length, size):
        words = [random_word(random.randint(1, length)) for _ in range(size)]
        shift = random.randint(1, 26)
        s = ' '.join(words)
        return [s, shift], s

    @staticmethod
    def _process(s, shift):
        secret = caesar_encode(s, shift)
        return caesar_decode(secret, shift)

    def test_all(self):
        src = inspect.getsource(caesar_decode)
        if src.find('lambda') == -1:
            pytest.fail('Ожидалось, что caesar_decode будет определен как lambda-функция')
        src = src.split(':')[-1].strip()
        if not re.fullmatch(r'caesar_encode\([^(]*\)', src):
            pytest.fail('Ожидалось, что caesar_decode будет состоять только из вызова caesar_encode')

        self._process.__name__ = 'encode_and_decode_back'
        runner = create(self._process, 'test_decode', self._gen)
        runner.multitest(
            runner.auto(length=10, size=10),
            runner.auto(length=10, size=100),
            runner.auto(length=100, size=10)
        )
