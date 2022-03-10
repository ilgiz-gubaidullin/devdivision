import pytest
import random

lst = [0, 'a', ['x', 'y']]

# 1) Список может содержать число, букву, вложенный список


@pytest.mark.parametrize('elem', lst)
def test_1(elem):
    assert elem in lst

# 2) Длина списка увеличится если добавить туда элемент


@pytest.fixture()
def random_number():
    return random.randint(0, 10)


def test_2(random_number):
    l1 = len(lst)
    l2 = lst.append(random_number)
    assert l1 != l2

# 3) Элемент из спиcка можно удалить


def test_3():
    elem = lst[0]
    del lst[0]
    assert elem not in lst

# 4) Список может быть пустым


class TestEmpty:
    def test_4(self):
        lst_empty = []
        assert len(lst_empty) == 0

# 5) Список можно изменить


def test_5():
    l1 = [0, 1]
    l1[0] = 1
    assert l1[0] == 1