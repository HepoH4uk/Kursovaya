from pathlib import Path
from typing import Any, Dict, List
from src.logger import setup_logging
import pandas as pd


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

    df = pd.read_excel(transactions)
    logger.info("Поиск значений по заданной строке")
    result = pd.DataFrame()
    for column in df.columns:
        filtered = df[df[column].astype(str).str.contains(search_str, case=False, na=False)]
        result = pd.concat([result, filtered])

    logger.info("Вывод отфильтрованных по заданной пользователем строке транзакций")
    if search_str == "" or search_str is None or not transactions:
        return []

    result = result.to_json(orient='records', force_ascii=False)
    return result


if __name__ == '__main__':
    search_str = "Супер"
    print(simple_search(search_str, file_excel))
