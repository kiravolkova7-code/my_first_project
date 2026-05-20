import json
import os


def load_operations(file_path: str) -> list:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if isinstance(data, list):
        return data
    return []
