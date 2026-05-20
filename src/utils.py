import json
import os
import logging

# Настройка логирования
logging.basicConfig(
    filename='logs/app_utils.log',
    filemode='w',
    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    encoding = 'utf-8'
)

def load_operations(file_path: str) -> list:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Файл успешно загружен: {file_path}")
    except (json.JSONDecodeError, OSError) as e:
        logging.error(f"Ошибка при чтении или декодировании файла {file_path}: {e}")
        return []

    if isinstance(data, list):
        logging.debug(f"Данные успешно загружены. Количество записей: {len(data)}")
        return data

    logging.warning(f"Данные в файле {file_path} не являются списком")
    return []