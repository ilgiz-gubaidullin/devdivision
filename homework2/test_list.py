import pytest
import random

lst = [0, 'a', ['x', 'y']]


@pytest.mark.parametrize('elem', lst)
def test_1(elem):
    """
    Список может содержать число, букву, вложенный список
    """
    assert elem in lst


@pytest.fixture()
def random_number():
    return random.randint(0, 10)


def test_2(random_number):
    """
    Длина списка увеличится если добавить туда элемент
    """
    l1 = len(lst)
    l2 = lst.append(random_number)
    assert l1 != l2


def test_3():
    """
    Элемент из спиcка можно удалить
    """
    elem = lst[0]
    del lst[0]
    assert elem not in lst


class TestEmpty:
    def test_4(self):
        """
        Список может быть пустым
        """
        lst_empty = []
        assert len(lst_empty) == 0


def test_5():
    """
    Список можно изменить
    """
    l1 = [0, 1]
    l1[0] = 1
    assert l1[0] == 1
