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

