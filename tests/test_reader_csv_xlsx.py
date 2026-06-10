import io
import pandas as pd
from unittest.mock import mock_open, patch

# --- Импортируем ваши функции ---
from src.reader_csv_xlsx import (
    _clean_string,
    _normalize_transaction,
    read_transactions_csv,
    read_transactions_excel
)


# Тесты для функции _clean_string
def test_clean_string_basic():
    assert _clean_string("  test\nstring\t") == "TESTSTRING"


def test_clean_string_with_nbsp():
    assert _clean_string("canceled\xa0") == "CANCELED"


def test_clean_string_none():
    assert _clean_string(None) == ""


def test_clean_string_empty():
    assert _clean_string("") == ""


# Тесты для функции _normalize_transaction
def test_normalize_transaction_full_data():
    test_row = {
        'id': '123',
        'state': ' executed ',
        'date': '2023-01-01',
        'amount': '100.50',
        'currency_name': 'Ruble',
        'currency_code': 'RUB',
        'from': 'acc1',
        'to': 'acc2',
        'description': 'Test payment'
    }

    expected_output = {
        'id': '123',
        'state': 'EXECUTED',
        'date': '2023-01-01',
        'from': 'acc1',
        'to': 'acc2',
        'description': 'Test payment',
        'operationAmount': {
            'amount': '100.50',
            'currency': {
                'name': 'Ruble',
                'code': 'RUB'
            }
        }
    }

    result = _normalize_transaction(test_row)
    assert result == expected_output


# Тесты для функции read_transactions_csv
def test_read_transactions_csv_success():
    csv_data = """id;state;date;amount;currency_name;currency_code;from;to;description
1;EXECUTED;2023-01-01;100;Ruble;RUB;acc1;acc2;Test payment"""

    # Создаем file-like объект из строки
    file_like = io.StringIO(csv_data)

    # Патчим функцию open, чтобы она возвращала наш объект
    with patch('builtins.open', return_value=file_like):
        transactions = read_transactions_csv('dummy_path.csv')

    assert len(transactions) == 1
    tx = transactions[0]
    assert tx['id'] == '1'
    assert tx['state'] == 'EXECUTED'


# Тесты для функции read_transactions_excel
def test_read_transactions_excel_success():
    # Создаем DataFrame с данными
    data = {
        'id': ['3'],
        'state': ['PENDING'],
        'date': ['2023-01-03'],
        'amount': [300],
        'currency_name': ['Euro'],
        'currency_code': ['EUR'],
        'from': ['acc5'],
        'to': ['acc6'],
        'description': ['Pending payment']
    }
    df = pd.DataFrame(data)

    # Патчим pandas.read_excel, чтобы он возвращал наш DataFrame
    with patch('pandas.read_excel', return_value={'Sheet1': df}):
        transactions = read_transactions_excel('dummy_path.xlsx')

    assert len(transactions) == 1
    tx = transactions[0]
    assert tx['id'] == '3'
    assert tx['state'] == 'PENDING'