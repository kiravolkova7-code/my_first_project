import pytest
import pandas as pd
from src.reader_csv_xlsx import read_transactions_csv, read_transactions_excel


# Тесты для CSV-ридера
def test_read_transactions_csv_success(mocker):
    """
    Проверяет, что функция корректно читает CSV-файл.
    """
    csv_data = "id;state;date\n1;EXECUTED;2023-01-01\n2;PENDING;2023-01-02"
    mock_file = mocker.patch('builtins.open', mocker.mock_open(read_data=csv_data))
    expected_result = [
        {'id': '1', 'state': 'EXECUTED', 'date': '2023-01-01'},
        {'id': '2', 'state': 'PENDING', 'date': '2023-01-02'}
    ]
    result = read_transactions_csv('any_path.csv')

    assert result == expected_result
    mock_file.assert_called_once_with('any_path.csv', mode='r', encoding='utf-8')


#Тесты для Excel-ридера
def test_read_transactions_excel_success(mocker):
    """
    Проверяет, что функция корректно обрабатывает DataFrame из Excel.
    """
    mock_df = mocker.MagicMock()
    mock_df.dropna.return_value = mock_df
    expected_dicts = [{'id': '3', 'state': 'EXECUTED'}]
    mock_df.to_dict.return_value = expected_dicts
    mocker.patch('pandas.read_excel', return_value=mock_df)
    result = read_transactions_excel('dummy_path.xlsx')

    assert result == expected_dicts