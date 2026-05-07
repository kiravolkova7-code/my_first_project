def filter_by_state(items, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    """
    return [item for item in items if item.get('state') == state]


def sort_by_date(data, descending=True):
    """
    Сортирует список словарей по ключу 'date' (в формате ISO 8601).

    """
    # Создаем копию списка, чтобы не изменять исходные данные
    sorted_data = data.copy()

    # Используем встроенный метод sort с lambda-функцией в качестве ключа.
    # Сравнение строк в формате 'YYYY-MM-DDTHH:MM:SS...' работает корректно.
    sorted_data.sort(key=lambda x: x['date'], reverse=descending)

    return sorted_data