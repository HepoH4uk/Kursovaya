from pathlib import Path
from typing import Any, Dict, List
from src.logger import setup_logging


file_excel = "../data/operations.xlsx"

current_dir = Path(__file__).parent.parent.resolve()
file_path_log = current_dir/'../log', 'services.log'
logger = setup_logging('services', file_path_log)


def simple_search(search_str: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Функция, которая получает строку для поиска и список транзакций.
    Выводит список транзакций, в которых есть данная строка
    """

    if not isinstance(search_str, str):
        logger.info("Ошибка не корректного ввода данных")
        raise TypeError("Неверный тип данных")
    new_list_transactions = []
    logger.info("Поиск значений по заданной строке")
    for item in transactions:

        if search_str in str(item['id']):
            new_list_transactions.append(item)
        elif search_str in item['state']:
            new_list_transactions.append(item)
        elif search_str in item['date']:
            new_list_transactions.append(item)
        elif search_str in item['operationAmount']['amount']:
            new_list_transactions.append(item)
        elif search_str in item['operationAmount']['currency']['name']:
            new_list_transactions.append(item)
        elif search_str in item['operationAmount']['currency']['code']:
            new_list_transactions.append(item)
        elif search_str in item['description']:
            new_list_transactions.append(item)
        elif search_str in item['from']:
            new_list_transactions.append(item)
        elif search_str in item['to']:
            new_list_transactions.append(item)

    result = new_list_transactions
    logger.info("Вывод отфильтрованных по заданной пользователем строке транзакций")
    if search_str == "" or search_str is None or not transactions:
        return []

    print("Результат simple_search:", result)
    return result


transactions = (
    [
        {
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
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        }
    ]
)


if __name__ == '__main__':
    search_str = input('Введите строку поиска: ')
    simple_search(search_str, transactions)
