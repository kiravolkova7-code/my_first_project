def filter_by_state(items, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param items: список словарей, каждый из которых содержит ключ 'state'
    :param state: значение для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей с соответствующим значением state
    """
    return [item for item in items if item.get('state') == state]


