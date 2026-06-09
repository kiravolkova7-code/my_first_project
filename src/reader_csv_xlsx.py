import csv
import re
import pandas as pd
from datetime import datetime

def _clean_string(value):
    """
    Приводит строку к верхнему регистру и удаляет все непечатные символы.
    """
    if value is None:
        return ''
    # 1. Приводим к строке и верхнему регистру
    # 2. Удаляем все пробельные и управляющие символы
    return re.sub(r'[\s\r\n\t\xa0]+', '', str(value).upper())

def _normalize_transaction(row):
    """
    Приводит данные из плоского формата (CSV/XLSX) к вложенному формату (JSON).
    """
    # --- ИЗМЕНЕНИЕ: Очищаем поле 'state' сразу при чтении ---
    raw_state = row.get('state')
    cleaned_state = _clean_string(raw_state) if raw_state is not None else ''
    # ---------------------------------------------------------

    transaction = {
        'id': row.get('id'),
        'state': cleaned_state, # Используем очищенное значение
        'date': row.get('date'),
        'from': row.get('from'),
        'to': row.get('to'),
        'description': row.get('description'),
        'operationAmount': {
            'amount': str(row.get('amount', '')),
            'currency': {}
        }
    }

    # Заполняем вложенный словарь 'currency'
    currency = transaction['operationAmount']['currency']
    if 'currency_name' in row and row['currency_name'] is not None:
        currency['name'] = str(row.get('currency_name'))
    if 'currency_code' in row and row['currency_code'] is not None:
        currency['code'] = str(row.get('currency_code'))

    return transaction



def read_transactions_csv(file_path):
    """Читает транзакции из CSV-файла и нормализует их структуру."""
    transactions = []
    try:
        # Добавляем delimiter=';' чтобы парсер знал о разделителе
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            # --- НОВАЯ ДИАГНОСТИКА: ВЫВОД ИМЕН СТОЛБЦОВ ---
            print("[ДИАГНОСТИКА] Имена столбцов, найденные в CSV-файле:")
            print(reader.fieldnames)
            # ------------------------------------------------

            # --- НОВАЯ ДИАГНОСТИКА: ВЫВОД ПЕРВОЙ СТРОКИ ДАННЫХ ---
            try:
                first_row = next(reader)
                print("[ДИАГНОСТИКА] Первая строка данных из файла:")
                print(first_row)
            except StopIteration:
                print("[ДИАГНОСТИКА] В файле нет строк с данными (только заголовок).")
            # ---------------------------------------------------

            csvfile.seek(0)
            reader = csv.DictReader(csvfile, delimiter=';') # Указываем разделитель заново

            for row in reader:
                normalized_row = _normalize_transaction(row)
                transactions.append(normalized_row)

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении CSV-файла: {e}")

    return transactions


def read_transactions_excel(file_path):
    """Читает транзакции из XLSX-файла и нормализует их структуру."""
    transactions = []
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None, dtype=str)

        all_sheets_df = pd.concat(excel_data.values(), ignore_index=True)

        # --- НОВОЕ: Очистка имен столбцов от пробелов ---
        # Эта строка проходит по всем названиям столбцов и убирает пробелы по краям.
        all_sheets_df.columns = all_sheets_df.columns.str.strip()
        # ------------------------------------------------

        for _, row in all_sheets_df.iterrows():
            normalized_row = _normalize_transaction(row.to_dict())
            transactions.append(normalized_row)

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении Excel-файла: {e}")

    return transactions