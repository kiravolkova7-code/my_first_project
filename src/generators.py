def filter_by_currency(transactions, currency_code):
    """
    Возвращает итератор по транзакциям,
    где валюта операции соответствует currency_code.
    """
    for transaction in transactions:
        # Проверяем, что структура соответствует ожидаемой
        op_amount = transaction.get('operationAmount', {})
        currency = op_amount.get('currency', {})
        if currency.get('code') == currency_code:
            yield transaction


def transaction_descriptions(transactions):
    """
    Генератор, возвращающий поочерёдно описание каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get('description', '')


def card_number_generator(start, end):
    """
    Генератор, который выдаёт номера банковских карт в
    формате XXXX XXXX XXXX XXXX
    в заданном диапазоне от start до end (включительно)
    """
    for number in range(start, end + 1):
        # Форматируем число в строку из 16 цифр с ведущими нулями
        card_str = f"{number:016}"
        # Разбиваем на группы по 4 цифры
        formatted_card = " ".join([card_str[i:i+4] for i in range(0, 16, 4)])
        yield formatted_card
