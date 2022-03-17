import pytest


@pytest.fixture()
def prepared_str():
    return 'qwe'


def test_str_immute(prepared_str):
    """
    В строку нельзя добавлять новые элементы
    """
    str = prepared_str
    with pytest.raises(TypeError):
        str[0] = 1
        pytest.fail("No TypeError occurred")


@pytest.mark.parametrize('data', ('qwe!@#', 123, ['a', 'b'], {'q': 5}))
def test_str_contains(data):
    """
    В строку можно конвертировать другие типы данных
    """
    a = str(data)
    assert isinstance(a, str)


def test_str_reg():
    """
    Содержание строки зависит от регистра
    """
    a = 'qwe'
    b = 'Qwe'
    assert a != b


def test_str_elem():
    """
    Нельзя удалить элемент строки
    """
    with pytest.raises(TypeError):
        a = 'hello'
        del a[0]
        pytest.fail('No TypeError occurred')


class TestStrCount:
    def test_str_in(self):
        """
        Строка может содержать элемент несколько раз
        """
        a = 'qweq'
        assert a.count('q') == 2
