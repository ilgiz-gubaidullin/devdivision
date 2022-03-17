import pytest


@pytest.fixture()
def prepared_dict():
    return dict(a=1, b=2)


def test_same_keys(prepared_dict):
    """
    Тест на возможность добавить 2 одинаковых ключа
    Двух одинаковых ключей в словаре быть не может, остается только последнее добавленное
    """
    d = prepared_dict
    d['a'] = 'new_value'
    assert d['a'] == 'new_value'


@pytest.mark.parametrize('elem', (3, 'xx', [1, 2], {'w': 0}))
def test_dict_keys(elem, prepared_dict):
    """
    Ключом словаря может быть только неизменяемое значение
    """
    try:
        d = prepared_dict
        d[elem] = 1
    except TypeError:
        print(f"Element as {elem} can not be dictionary key")


@pytest.mark.parametrize('elem', (3, 'xx', [1, 2], {'w': 0}))
def test_dict_val(elem, prepared_dict):
    """
    Значением словаря может быть любое значение
    """
    d = prepared_dict
    d['c'] = elem


def test_miss_key(prepared_dict):
    """
    Если запросить из словаря несуществующий элемент, то возникнет ошибка KeyError
    """
    with pytest.raises(KeyError):
        d = prepared_dict
        assert d['c']
        pytest.fail('No KeyError occurred')


class TestDictGet:
    def test_get_method(self, prepared_dict):
        '''
        Если использовать метод get в форме записи dictionary.get(key, val),
        метод возвращает значение val, если элемент с ключом key отсутствует в списке
        '''
        d = prepared_dict
        assert d.get('c', 3) == 3
