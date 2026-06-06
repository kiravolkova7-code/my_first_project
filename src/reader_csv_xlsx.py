import csv
import pandas as pd


def read_transactions_csv(csv_path: str):
    """
    Считывает финансовые операции из CSV-файла.
    """
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        transactions = list(reader)
    return transactions


def read_transactions_excel(xlsx_path: str):
    """
    Считывает финансовые операции из Excel-файла (с первого листа).
    """
    df = pd.read_excel(xlsx_path, sheet_name=0)
    df = df.dropna(how='all')  # Исключаем полностью пустые строки
    transactions = df.to_dict(orient='records')
    return transactions
