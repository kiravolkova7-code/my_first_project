# Тесты для API
import pytest
import requests
from src.external_api import convert_to_rub, get_transaction_amount_in_rub


def test_convert_rub_to_rub():
    """Если валюта уже RUB, сумма должна возвращаться без изменений."""
    assert convert_to_rub(150.5, 'RUB') == 150.5


def test_convert_usd_success(mocker):
    """Тест успешной конвертации USD в RUB."""
    # 1. Создаем "поддельный" ответ от API
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'result': 9200.5}
    mock_response.raise_for_status.side_effect = None  # Ошибок нет

    # 2. Подменяем вызов requests.get, чтобы он возвращал наш mock-ответ
    mocker.patch('src.external_api.requests.get', return_value=mock_response)

    # 3. Вызываем функцию и проверяем результат
    result = convert_to_rub(100, 'USD')
    assert result == 9200.5


def test_api_key_not_found(mocker):
    """Тест ошибки, если API-ключ не найден."""
    # Подменяем значение переменной API_KEY на None
    mocker.patch('src.external_api.API_KEY', None)

    with pytest.raises(RuntimeError, match="API-ключ не найден"):
        convert_to_rub(100, 'USD')


def test_http_error_401(mocker):
    """Тест обработки HTTP-ошибки (например, 401 Unauthorized)."""
    # Создаем ответ с ошибкой
    mock_response = mocker.Mock()

    # Настраиваем выброс исключения при вызове raise_for_status()
    http_error = requests.HTTPError("401 Unauthorized")
    mock_response.raise_for_status.side_effect = http_error

    mocker.patch('src.external_api.requests.get', return_value=mock_response)

    with pytest.raises(RuntimeError) as exc_info:
        convert_to_rub(100, 'USD')

    assert "Ошибка соединения с API" in str(exc_info.value)


# Тесты для get_transaction_amount_in_rub
def test_transaction_valid_usd(mocker):
    """Тест успешной обработки транзакции в USD."""
    # Мочим функцию конвертации, чтобы не делать реальный запрос
    mocker.patch('src.external_api.convert_to_rub', return_value=9200.5)

    transaction = {'amount': 100, 'currency': 'USD'}

    result = get_transaction_amount_in_rub(transaction)

    assert result == 9200.5


def test_transaction_no_currency_defaults_to_rub(mocker):
    """Если в транзакции нет поля 'currency', должно использоваться значение по умолчанию ('RUB')."""
    mocker.patch('src.external_api.convert_to_rub', return_value=500)

    transaction = {'amount': 500}  # Нет ключа 'currency'

    result = get_transaction_amount_in_rub(transaction)

    assert result == 500


def test_transaction_invalid_amount_type():
    """Тест ошибки, если сумма транзакции не является числом."""
    transaction = {'amount': 'сто рублей', 'currency': 'USD'}

    with pytest.raises(ValueError, match="Сумма транзакции должна быть числом."):
        get_transaction_amount_in_rub(transaction)
