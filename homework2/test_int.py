import random
import pytest


def test_int_let():
    """
    int не может содержать строку
    """
    with pytest.raises(ValueError):
        a = int('qwe')
        pytest.fail('No ValueError occurred')


@pytest.fixture()
def float_num():
    return random.uniform(0.1, 3.1)


def test_int_ln(float_num):
    """
    int может содержать только целые числа
    """
    a = 1.01
    b = int(a)
    assert a != b


@pytest.mark.parametrize('cs, res', ((bin, '0b1010'), (oct, '0o12'), (hex, '0xa')))
def test_int_cs(cs, res):
    """
    Целые числа могут быть преобразованы в другую систему счисления
    """
    number = 10
    assert cs(number) == res


class TestInt:
    def test_int_str(self):
        """
        В int можно конвертировать строку, которая содержит только целые числа
        """
        a = '19'
        assert isinstance(int(a), int)


def test_int_er():
    """
    В int нельзя конвертировать строку, которая содержит только НЕ целые числа
    """
    with pytest.raises(ValueError):
        a = '19.5'
        int(a)
        pytest.fail('No ValueError occurred')
