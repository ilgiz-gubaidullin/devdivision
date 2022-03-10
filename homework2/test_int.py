import random

import pytest


# 1) int не может содержать буквы


def test_int_let():
    with pytest.raises(ValueError):
        a = int('qwe')
        pytest.fail('No ValueError occurred')


# 2) int может содержать только целые числа


def test_int_ln():
    a = 1.01
    b = int(a)
    assert a != b


# 3) Целые числа могут быть преобразованы в другую систему счисления


@pytest.fixture()
def prepared_num():
    return random.randint(0, 3)


@pytest.mark.parametrize('cs', (bin, oct, hex))
def test_int_cs(cs, prepared_num):
    a = prepared_num
    cs(a)


# 4) В int можно конвертировать строку которая содержит только целые числа

class TestInt:
    def test_int_str(self):
        a = '19'
        assert type(int(a)) is int


# 5) В int нельзя конвертировать строку которая содержит только НЕ целые числа


def test_int_er():
    with pytest.raises(ValueError):
        a = '19.5'
        int(a)
        pytest.fail('No ValueError occurred')