import pandas as pd
import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_exchange = os.getenv("API_KEY_exchange")
API_KEY_sp = os.getenv("API_KEY_sp")

file_excel = "../data/operations.xlsx"


def greetings():
    """Функция, которая приветствует пользователя в зависимости от текущего времени суток """

    current_date_time = datetime.datetime.now()
    hour = current_date_time.hour
    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"


# def interesting_date():
#     print('Введите интересующую вас дату')
#     day = int(input('День: '))
#     while True:
#         if day > 31 or day <= 0:
#             print("День введен не корректно,пожалуйста повторите попытку")
#             day = int(input('День: '))
#         else:
#             break
#     manth = int(input('Месяц: '))
#     while True:
#         if manth > 12 or manth <= 0:
#             print("Месяц введен не корректно,пожалуйста повторите попытку")
#             manth = int(input('Месяц: '))
#         else:
#             break
#     year = int(input('Год: '))
#     while True:
#         if year > 2030 or year <= 1999:
#             print("Год введен не корректно,пожалуйста повторите попытку")
#             year = int(input('Год: '))
#         else:
#             break
#     if day < 10 and manth < 10:
#         date = f"0{day}.0{manth}.{year}"
#     elif day < 10:
#         date = f"0{day}.{manth}.{year}"
#     elif manth < 10:
#         date = f"{day}.0{manth}.{year}"
#     return date


def user_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает детали транзакций для каждой карты:
    - последние 4 цифры карты
    - общие расходы
    - кэшбек (1 рубль за каждые 100 рублей расхода)
    """
    df = pd.read_excel(file_excel)

    df_filtered = df.loc[(pd.to_datetime(df['Дата операции'], dayfirst=True) <= data_time) &
                         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))].copy()

    df_filtered.loc[:, 'кэшбек'] = df_filtered['Сумма операции с округлением'] // 100
    sales_by_card = df_filtered.groupby('Номер карты')[['Сумма операции с округлением', 'кэшбек']].sum()
    sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)

    return sorted_sales


def max_five_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает 5 лучших транзакций по сумме платежа.
    """
    df = pd.read_excel(file_excel)
    filtered_df = df.copy()

    filtered_df = df.loc[
        (pd.to_datetime(filtered_df['Дата операции'], dayfirst=True) <= data_time) &
        (pd.to_datetime(filtered_df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))
    ]
    top_five_transactions = filtered_df.sort_values(by='Сумма операции с округлением', ascending=False).head(5)

    return top_five_transactions


def exchange_rate() -> list:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
    """
    currency_list = ["USD", "EUR"]
    convert_to = "RUB"
    new_currency_list = []

    for currency in currency_list:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={currency}&amount=1"
        headers = {"apikey": API_KEY_exchange}

        response = requests.get(url, headers=headers)
        result = response.json()
        currency_value = result.get('result')

        if currency_value is not None:
            new_currency_list.append(currency_value)
        else:
            print("Ошибка: ключ 'result' не найден в ответе для:", currency)

    return new_currency_list


def get_price_sp500() -> list:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
    """
    currencies_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    currencies_price = []

    for currency in currencies_list:
        response = requests.get(f"https://api.twelvedata.com/price?symbol={currency}&apikey={API_KEY_sp}")
        dict_result = response.json()
        price_element = dict_result.get('price')
        currencies_price.append(f"{currency}:{price_element}")

    return currencies_price
