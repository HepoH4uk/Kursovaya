from typing import Any

import pandas as pd

from src.reports import dir_transactions_excel, spending_by_category
from src.services import simple_search
from src.views import website


file_excel = "../data/operations.xlsx"


def main() -> Any:
    """Функция для запуска всего проекта"""
    print("Функция для запуска всего проекта")


if __name__ == '__main__':
    print("\nГЛАВНАЯ\n")

    data_time = "31.12.2021 00:00:00"
    result1, result2, result3, result4, result5 = website(pd.Timestamp((data_time)))
    print(result1, result2, result3, result4, result5)

    print("\nСервисы.Простой поиск\n")
    search_str = input('Введите строку поиска:\n ')
    simple_search(search_str, file_excel)

    print("\nОТЧЕТЫ\n")
    spending_by_category(pd.read_excel(dir_transactions_excel), 'Супермаркеты', '31.12.2021')
