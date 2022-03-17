import random
import pytest


# 1) int не может содержать буквы


def test_int_let():
    with pytest.raises(ValueError):
        a = int('qwe')
        pytest.fail('No ValueError occurred')


# 2) int может содержать только целые числа
@pytest.fixture()
def float_num():
    return random.uniform(0.1, 3.1)


def test_int_ln(float_num):
    a = 1.01
    b = int(a)
    assert a != b


# 3) Целые числа могут быть преобразованы в другую систему счисления


@pytest.mark.parametrize('cs, res', ((bin, '0b1010'), (oct, '0o12'), (hex, '0xa')))
def test_int_cs(cs, res):
    number = 10
    assert cs(number) == res


# 4) В int можно конвертировать строку, которая содержит только целые числа

class TestInt:
    def test_int_str(self):
        a = '19'
        assert isinstance(int(a), int)


# 5) В int нельзя конвертировать строку, которая содержит только НЕ целые числа


def test_int_er():
    with pytest.raises(ValueError):
        a = '19.5'
        int(a)
        pytest.fail('No ValueError occurred')