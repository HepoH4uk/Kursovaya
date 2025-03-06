from pathlib import Path
from typing import Any, Dict, List
from src.logger import setup_logging
import pandas as pd


dir_transactions_excel = "../data/operations.xlsx"

current_dir = Path(__file__).parent.parent.resolve()
file_path_log = current_dir/'../log', 'services.log'
logger = setup_logging('services', file_path_log)


def simple_search(search_str: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Функция, которая получает строку для поиска и список транзакций.
    Выводит список транзакций, в которых есть данная строка
    """
    new_list_transactions = []
    logger.info("Фильтр не корректных значений")
    if not isinstance(search_str, str):
        logger.info("Ошибка не корректного ввода данных")
        raise TypeError("Неверный тип данных")

    if search_str == "" or search_str is None or not transactions:
        return []

    df = pd.read_excel(transactions) if isinstance(transactions, pd.DataFrame) else transactions
    logger.info("Поиск значений по заданной строке")
    result = pd.DataFrame()
    try:
        for column in df.columns:
            filtered = df[df[column].astype(str).str.contains(search_str, case=False, na=False)]
            result = pd.concat([result, filtered])
        return result
    except AttributeError:
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
        return new_list_transactions

    # result = json.dumps(new_list_transactions)
    logger.info("Вывод отфильтрованных по заданной пользователем строке транзакций")
    return result


if __name__ == '__main__':
    search_str = "Супер"
    print(simple_search(search_str, dir_transactions_excel))
