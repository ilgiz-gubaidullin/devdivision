import random

import pytest


def test_exception():
    """
    Если удалить несуществующий элемент при помощи remove, то возникнет ошибка KeyError
    """
    st = {1, 2, 3}
    with pytest.raises(KeyError):
        st.remove(4)
        pytest.fail('No KeyError occurred')


data_col = [
    (
        ['a', 'a', 'c']
    ),
    (
        ['a', 'a', 'a', 'c']
    ),
    (
        [1, 1, 2]
    )
]


class TestUnique:
    @pytest.mark.parametrize('data_type', data_col)
    def test_unique_value(self, data_type):
        """
        В множестве хранятся только уникальные элементы
        """
        st = set(data_type)
        assert len(st) == 2


@pytest.fixture()
def random_list():
    return random.sample(range(10), 3)


def test_add_list(random_list):
    """
    В множество нельзя добавить изменяемый элемент(список)
    """
    with pytest.raises(TypeError):
        st = {1, 2, 3}
        st.add(random_list)
        pytest.fail('No TypeError occurred')


def test_frozen_set():
    """
    Вид множества frozenset является неизменяемым множеством
    """
    with pytest.raises(AttributeError):
        a = frozenset('halo')
        a.add(1)
        pytest.fail('No AttributeError occurred')


def test_set_order():
    """
    В множествах элементы могут находится в любом порядке
    """
    a = {1, 2, 3}
    b = {3, 2, 1}
    assert a == b
