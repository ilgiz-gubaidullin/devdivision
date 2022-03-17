import pytest

@pytest.fixture()
def prepared_dict():
    return dict(a=1, b=2)

# 1) Тест на возможность добавить 2 одинаковых ключа


def test_same_keys(prepared_dict):
    """
    Двух одинаковых ключей в словаре быть не может, остается только последнее добавленное
    """
    d = prepared_dict
    d['a'] = 'new_value'
    assert d['a'] == 'new_value'


# 2) Ключом словаря может быть только неизменяемое значение


@pytest.mark.parametrize('elem', (3, 'xx', [1, 2], {'w': 0}))
def test_dict_keys(elem, prepared_dict):
    try:
        d = prepared_dict
        d[elem] = 1
    except TypeError:
        print(f"Element as {elem} can not be dictionary key")


# 3) Значением словаря может быть любое значение


@pytest.mark.parametrize('elem', (3, 'xx', [1, 2], {'w': 0}))
def test_dict_val(elem, prepared_dict):
    d = prepared_dict
    d['c'] = elem


# 4) Если запросить из словаря несуществующий элемент то возникнет ошибка KeyError


def test_miss_key(prepared_dict):
    with pytest.raises(KeyError):
        d = prepared_dict
        assert d['c']
        pytest.fail('No KeyError occurred')


# 5) Если использовать метод get в форме записи dictionary.get(key, val), метод возвращает значение val, если элемент с ключом key отсутствует в списке


class TestDictGet:
    def test_get_method(self, prepared_dict):
        d = prepared_dict
        assert d.get('c', 3) == 3
