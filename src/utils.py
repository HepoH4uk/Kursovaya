import json
import pandas as pd
import datetime
import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from src.logger import setup_logging


load_dotenv()
API_KEY_exchange = os.getenv("API_KEY_exchange")
API_KEY_sp = os.getenv("API_KEY_sp")

file_excel = "../data/operations.xlsx"
current_dir = Path(__file__).parent.parent.resolve()
file_path_log = current_dir/'../log', 'utils.log'

logger = setup_logging('utils', file_path_log)


def greetings(date_time: str = None) -> str:
    """Функция, которая приветствует пользователя в зависимости от текущего времени суток """
    try:
        logger.info("Определяем было ли передано значение времени")
        if date_time is None:
            current_date_time = datetime.datetime.now()
        else:
            current_date_time = pd.Timestamp(date_time)
        hour = current_date_time.hour
        logger.info("Определяем время суток в соответствии с временем")
        if 0 <= hour < 6:
            return "Доброй ночи"
        elif 6 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 24:
            return "Добрый вечер"
    except ValueError:
        logger.error("Передано неверное время")
        raise ValueError("Неверный формат времени")
    except Exception:
        logger.error("Произошла ошибка")
        raise Exception("Произошла ошибка")


def user_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает детали транзакций для каждой карты:
    - последние 4 цифры карты
    - общие расходы
    - кэшбек (1 рубль за каждые 100 рублей расхода)
    """
    data_time = pd.Timestamp(data_time)
    logger.info("Читаем excel-файл")
    df = pd.read_excel(file_excel)
    logger.info("Определяем период времени подсчета времени")
    df_filtered = df.loc[(pd.to_datetime(df['Дата операции'], dayfirst=True) <= data_time) &
                         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))].copy()
    logger.info("Производим необходимые операции")
    df_filtered.loc[:, 'кэшбек'] = df_filtered['Сумма операции с округлением'] // 100
    sales_by_card = df_filtered.groupby('Номер карты')[['Сумма операции с округлением', 'кэшбек']].sum().reset_index()
    sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)
    result = sorted_sales.to_json(orient='records', force_ascii=False)
    return result


def max_five_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает 5 лучших транзакций по сумме платежа.
    """
    logger.info("Читаем excel-файл")
    df = pd.read_excel(file_excel)
    data_time = pd.Timestamp(data_time)
    filtered_df = df.copy()
    logger.info("Определяем период подсчета времени")
    filtered_df = df.loc[
        (pd.to_datetime(filtered_df['Дата операции'], dayfirst=True) <= data_time) &
        (pd.to_datetime(filtered_df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))
    ]
    logger.info("Определяем 5 лучших транзакций по сумме платежа")
    top_five_transactions = filtered_df.sort_values(by='Сумма операции с округлением', ascending=False).head(5)
    result = top_five_transactions.to_json(orient='records', force_ascii=False)

    return result


def exchange_rate() -> list:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
    """
    currency_list = ["USD", "EUR"]
    convert_to = "RUB"
    new_currency_list = []
    logger.info("Отправляем запрос на конвертацию валют")
    try:
        for currency in currency_list:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={currency}&amount=1"
            headers = {"apikey": API_KEY_exchange}

            response = requests.get(url, headers=headers)
            result = response.json()
            currency_value = result.get('result')

            if currency_value is not None:
                new_currency_list.append(currency_value)
            else:
                logger.info("Ошибка: ключ 'result' не найден")
                print("Ошибка: ключ 'result' не найден в ответе для:", currency)
        result = json.dumps(new_currency_list)

        return result

    except Exception:
        logger.info(f"Произошла ошибка: {Exception}")
        print(f"Произошла ошибка: {Exception}")


def get_price_sp500() -> list:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
    """
    currencies_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    currencies_price = []
    try:
        logger.info("Отправляем запрос на получение цен акций")
        for currency in currencies_list:
            response = requests.get(f"https://api.twelvedata.com/price?symbol={currency}&apikey={API_KEY_sp}")
            dict_result = response.json()
            price_element = dict_result.get('price')
            currencies_price.append(f"{currency}:{price_element}")
        result = json.dumps(currencies_price)
        return result
    except Exception:
        logger.info(f"Произошла ошибка: {Exception}")
        print(f"Произошла ошибка: {Exception}")
