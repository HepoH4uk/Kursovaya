from src.views import website
from datetime import datetime


def test_website():
    '''Тестирование правильности работы функции'''
    data_time = datetime.now()
    result = website(data_time)

    assert isinstance(result, tuple)
    assert len(result) == 5

    assert isinstance(result[0], str)
