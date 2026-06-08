import re
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет записи о банковских операциях, содержащие заданную строку в описании.
    """
    pattern = re.compile(search, re.IGNORECASE)

    # Фильтрация данных: оставляем только те словари, где в описании есть совпадение
    result = [item for item in data if 'description' in item and pattern.search(item['description'])]

    return result


def process_bank_operations(data: List[Dict], categories: list) -> dict:
    """
    Подсчитывает количество банковских операций для каждой заданной категории.
    Категория считается найденной, если её название присутствует как отдельное слово
    или часть строки
    в поле 'description' операции. Поиск выполняется без учёта регистра.
    """
    if not categories:
        return {}

    result = {category: 0 for category in categories}

    escaped_categories = [re.escape(category) for category in categories]
    pattern = re.compile("|".join(escaped_categories), re.IGNORECASE)

    for operation in data:
        description = operation.get('description')
        if description is None:
            continue

        found_categories = pattern.findall(description)

        # Увеличиваем счётчик для каждой найденной категории
        for cat in found_categories:
            for key in result:
                if key.lower() == cat.lower():
                    result[key] += 1
                    break

    return result
