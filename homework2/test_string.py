import pytest


@pytest.fixture()
def prepared_str():
    return 'qwe'


# 1) В строку нельзя добавлять новые элементы


def test_str_immute(prepared_str):
    str = prepared_str
    with pytest.raises(TypeError):
        str[0] = 1
        pytest.fail("No TypeError occurred")


# 2) В строку можно конвертировать другие типы данных


@pytest.mark.parametrize('data', ('qwe!@#', 123, ['a', 'b'], {'q': 5}))
def test_str_contains(data):
    a = str(data)
    assert isinstance(a, str)

# 3) Содержание строки зависит от регистра


def test_str_reg():
    a = 'qwe'
    b = 'Qwe'
    assert a != b


# 4) Нельзя удалить элемент строки


def test_str_elem():
    with pytest.raises(TypeError):
        a = 'hello'
        del a[0]
        pytest.fail('No TypeError occurred')


# 5) Строка может содержать элемент несколько раз


class TestStrCount:
    def test_str_in(self):
        a = 'qweq'
        assert a.count('q') == 2