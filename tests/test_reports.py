import pytest
import pandas as pd
from src.reports import spending_by_category, save_report
import os
import json


@pytest.fixture
def cleanup_files():
    yield
    # Удаляем файлы после теста
    files = os.listdir('data')
    for file in files:
        if file.startswith('report_dummy_function'):
            os.remove(os.path.join('data', file))


def test_save_report_creates_file(cleanup_files):
    @save_report()
    def dummy_function():
        return {"key": "value"}

    dummy_function()

    # Проверь, что файл создан
    files = os.listdir('data')
    assert any(file.startswith('report_dummy_function') for file in files)

    # Проверь содержимое файла
    file_path = os.path.join('data', files[0])
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data == {"key": "value"}


transactions_data = {
    'Категория': ['Фастфуд', 'Фастфуд', 'Развлечения'],
    'Дата операции': ['10.11.2019', '12.11.2019', '15.11.2019'],
    'Сумма': [100, 150, 200]
}
transactions_df = pd.DataFrame(transactions_data)


# Тест функции
@pytest.mark.parametrize("category, date, expected_count", [
    ('Фастфуд', '11.11.2019', 98),
    ('Фастфуд', None, 0),  # Проверка с текущей датой
    ('Развлечения', '11.11.2019', 0),
])
def test_spending_by_category(category, date, expected_count):
    result = spending_by_category(transactions_df, category, date)
    assert len(result) == expected_count


if __name__ == "__main__":
    pytest.main()
