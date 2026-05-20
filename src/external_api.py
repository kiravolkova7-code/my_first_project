import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения при импорте модуля
load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/convert'


def convert_to_rub(amount: float, currency: str) -> float:
    """
    Конвертирует сумму из USD или EUR в рубли по текущему курсу.
    """
    if not API_KEY or API_KEY == 'your_api_key_here':
        raise RuntimeError("API-ключ не найден или не настроен. Проверьте файл .env.example")

    currency = currency.upper()
    if currency == 'RUB':
        return amount

    params = {
        'to': 'RUB',
        'from': currency,
        'amount': amount,
        'apikey': API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Вызовет ошибку для 4xx/5xx статусов

        data = response.json()

        if 'result' in data:
            return float(data['result'])

        # Обработка ошибок, если они пришли в теле ответа
        error_info = data.get('error', {}).get('info') or data.get('type')
        raise ValueError(f"Ошибка API: {error_info}")

    except requests.HTTPError as http_err:
        raise RuntimeError(f"Ошибка соединения с API: {http_err}")


def get_transaction_amount_in_rub(transaction: dict) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях.
    transaction: {'amount': float, 'currency': str}
    """
    amount = transaction.get('amount')
    currency = transaction.get('currency', 'RUB')

    if not isinstance(amount, (int, float)):
        raise ValueError("Сумма транзакции должна быть числом.")

    return convert_to_rub(amount, currency)
