import re
from typing import List, Dict
from collections import Counter

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
    Подсчитывает количество банковских операций для каждой заданной категории,
    используя Counter из collections.
    Категория считается найденной, если её название присутствует как отдельное слово
    или часть строки в поле 'description' операции. Поиск выполняется без учёта регистра.
    """
    if not categories or not data:
        return {}

    # Экранируем спецсимволы в названиях категорий
    escaped_categories = [re.escape(category) for category in categories]

    # Компилируем единый паттерн для поиска всех категорий
    pattern = re.compile("|".join(escaped_categories), re.IGNORECASE)

    counter = Counter()

    for operation in data:
        description = operation.get('description')
        if not description:
            continue

        # Находим все упоминания ЛЮБЫХ категорий в этом описании
        found_in_desc = pattern.findall(description)

        # Используем set() чтобы одна операция засчитывалась только один раз для одной категории
        # (если слово повторяется в описании несколько раз)
        unique_found = {word.lower() for word in found_in_desc}
        counter.update(unique_found)

    # Финальный результат: собираем словарь по исходному списку категорий
    # .get(cat.lower(), 0) ищет ключ в нижнем регистре, что решает проблему с разным регистром
    result = {category: counter.get(category.lower(), 0) for category in categories}

    return result