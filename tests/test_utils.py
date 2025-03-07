import pytest
import pandas as pd
from unittest import mock
from src.utils import greetings, user_transactions, max_five_transactions, exchange_rate
from datetime import datetime


data = {
    'Дата операции': ['29.09.2018', '30.09.2018', '01.10.2018'],
    'Номер карты': ['*7197', '*4556', '*7197'],
    'Сумма операции с округлением': [186388.77, 181404.21, 150000.00]
}

df = pd.DataFrame(data)


def mock_read_excel(file):
    return df


def test_greetings():
    hour = pd.Timestamp.now().hour
    greeting = greetings()

    if 0 <= hour < 6:
        assert greeting == "Доброй ночи"
    elif 6 <= hour < 12:
        assert greeting == "Доброе утро"
    elif 12 <= hour < 18:
        assert greeting == "Добрый день"
    elif 18 <= hour < 24:
        assert greeting == "Добрый вечер"


def test_user_transactions(monkeypatch):
    monkeypatch.setattr(pd, "read_excel", mock_read_excel)
    test_date = pd.to_datetime('29-09-2018', dayfirst=True)
    result = user_transactions(test_date)

    expected = pd.DataFrame({
        'Номер карты': ['*7197'],
        'Сумма операции с округлением': [186388.77],
        'кэшбек': [1863.0]
    })

    pd.testing.assert_frame_equal(result, expected)


transactions_data = {
    'Дата операции': [
        '01.10.2023 17:01:37', '05.10.2023 17:01:37', '10.10.2023 17:01:37',
        '15.10.2023 17:01:37', '20.10.2023 17:01:37', '25.10.2023 17:01:37'
    ],
    'Сумма операции с округлением': [100, 200, 300, 400, 500, 600]
}

df_test = pd.DataFrame(transactions_data)


def test_max_five_transactions(monkeypatch):
    monkeypatch.setattr(pd, "read_excel", lambda _: df_test)
    test_date = datetime(2023, 10, 21, 00, 00, 00)

    expected_result = df_test.loc[0:4].sort_values(
        by='Сумма операции с округлением', ascending=False
    ).head(5)

    result = max_five_transactions(test_date)

    result = result.reset_index(drop=True)
    expected_result = expected_result.reset_index(drop=True)
    print(expected_result)
    print(result)
    pd.testing.assert_frame_equal(result, expected_result)


@mock.patch('requests.get')
def test_exchange_rate(mock_requests_get):
    mock_requests_get.side_effect = [
        mock.Mock(json=lambda: {
            "success": True,
            "result": 23.23
        }),
        mock.Mock(json=lambda: {
            "success": True,
            "result": 31.23
        })
    ]
    result = exchange_rate()
    expected = [23.23, 31.23]

    assert result == expected


if __name__ == "__main__":
    pytest.main()
