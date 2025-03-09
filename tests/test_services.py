import pytest
from src.services import simple_search


@pytest.fixture
def coll():
    return [{
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                                }
                                },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
            }]


def test_simple_search(coll):
    '''Тестирование правильности работы функции'''
    expected_result = coll  # Ожидаемый список транзакций
    assert simple_search(search_str="RUB", transactions=coll) == expected_result


def test_simple_search_not_search_str(coll):
    '''Тестирование правильности работы функции при отсутствии search_str'''

    assert simple_search(search_str="", transactions=coll) == []


def test_simple_search_not_transactions(coll):
    '''Тестирование правильности работы функции при отсутствии transactions'''

    assert simple_search(search_str="RUB", transactions="") == []


def test_simple_search_error_search_str(coll):
    '''Тестирование правильности работы функции при отсутствии search_str в transactions'''

    assert (simple_search(search_str="fG", transactions=coll)) == []


def test_simple_search_not_str_search_str(coll):
    '''Тестирование правильности работы функции при неверном типе данных search_str'''

    with pytest.raises(TypeError, match="Неверный тип данных"):
        simple_search(search_str=11, transactions=coll)


def test_simple_search_type_error():
    '''Тест на выпадение ошибки при вводе неверного типа данных'''

    transactions = [{'description': 'покупка'}, {'description': 'оплата'}]
    with pytest.raises(TypeError, match="Неверный тип данных"):
        simple_search(search_str=123, transactions=transactions)


if __name__ == "__main__":
    pytest.main()
