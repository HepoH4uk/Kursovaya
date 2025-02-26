from src.logger import setup_logging
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import pandas as pd


current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir/'data'/'operations.xlsx'
file_path_log = current_dir/'../log', 'reports.log'


logger = setup_logging('reports', file_path_log)


def save_report(filename=None):
    """Декоратор для записи отчета в файл."""
    def wrapper(func):
        def inner(*args, filename: Optional[str] = None, **kwargs):
            result = func(*args, **kwargs)
            print("Аргументы функции:", args, kwargs)

            if filename is None:
                file_name = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            logger.info("Сохранение результата в файл data/file")
            if not os.path.exists('data'):
                os.makedirs('data')
            file_path = f'data/{file_name}'

            def save_to_file(data, file_path):
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

            save_to_file(result, file_path)
            print("Результат функции:", result)

            return result
        return inner
    return wrapper


@save_report()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    '''
    Функция, которая принимает на вход: датафрейм с транзакциями, название категории,
    опциональную дату. Если дата не передана, то берется текущая дата. Функция возвращает
    траты по заданной категории за последние три месяца (от переданной даты).
    '''

    if date is None:
        date = datetime.now().date()

    try:
        date = pd.to_datetime(date, dayfirst=True)
    except ValueError:
        raise ValueError("Неверный формат даты. Корректный формат: 'dd.mm.yyyy'.")

    df = pd.read_excel(dir_transactions_excel) if isinstance(transactions, pd.DataFrame) else transactions
    filtered_transactions = df[df['Категория'] == category]

    start_date = date - timedelta(days=90)
    end_date = date

    logger.info("Фильтрация по заданной категории")
    recent_transactions = filtered_transactions[
        (pd.to_datetime(filtered_transactions['Дата операции'], dayfirst=True) >= start_date) &
        (pd.to_datetime(filtered_transactions['Дата операции'], dayfirst=True) <= end_date)
    ]

    logger.info("Траты по заданной категории за последние 3 месяца от переданной даты")

    return recent_transactions.to_dict('records')


if __name__ == '__main__':
    spending_by_category(pd.read_excel(dir_transactions_excel), 'Супермаркеты', '31.12.2021')
