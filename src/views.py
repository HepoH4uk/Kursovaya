from src.utils import (greetings, exchange_rate, get_price_sp500, max_five_transactions, user_transactions)
from typing import Union
import pandas as pd
import datetime
from pathlib import Path
from dotenv import load_dotenv
import json


load_dotenv('../.env')

dir_transactions_excel = Path(__file__).parent.parent.resolve()

file_excel = dir_transactions_excel/'data'/'operations.xlsx'
print(file_excel)


def website(data_time: datetime) -> Union[list, dict]:

    """
    Главная функция, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:
    Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости
    от текущего времени.
    По каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    Топ-5 транзакций по сумме платежа.
    Курс валют.
    Стоимость акций из S&P500.
    """
    print(f"Входные данные: {data_time}")
    result1 = greetings(data_time)
    result2 = user_transactions(data_time).to_json(orient='records', force_ascii=False)
    result3 = max_five_transactions(data_time).to_json(orient='records', force_ascii=False)
    result4 = json.dumps(exchange_rate())
    result5 = json.dumps(get_price_sp500())

    return result1, result2, result3, result4, result5


if __name__ == '__main__':

    print(greetings())
    data_time = str("31-12-2021 00:00:00")
    result = user_transactions(pd.Timestamp(data_time))
    print("Результат транзакций:")
    print(result)
    print(f"Пять максимальных транзакций: {max_five_transactions(pd.Timestamp(data_time))}")
    print(f"Курс валют: {exchange_rate()}")
    print(f"Стоимость акций из SP500: {get_price_sp500()}")
