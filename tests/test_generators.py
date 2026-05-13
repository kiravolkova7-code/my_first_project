# Для первой функции
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
import pytest


def test_filter_usd(transactions):
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 2
    assert usd_transactions[0]["id"] == 1
    assert usd_transactions[1]["id"] == 3


def test_filter_eur(transactions):
    eur_transactions = list(filter_by_currency(transactions, "EUR"))
    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 2


def test_filter_missing_currency(transactions):
    jpy_transactions = list(filter_by_currency(transactions, "JPY"))
    assert jpy_transactions == []


def test_empty_list():
    empty_transactions = list(filter_by_currency([], "USD"))
    assert empty_transactions == []


def test_no_matching_currency(transactions):
    no_cny = list(filter_by_currency(transactions, "CNY"))
    assert no_cny == []


# Для второй функции
def test_descriptions_match_transactions(sample_transactions):
    # Преобразуем генератор в список для удобства проверки
    descriptions = list(transaction_descriptions(sample_transactions))
    # Проверяем, что количество и содержание совпадают
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
    ]


def test_empty_list_two():
    # Проверяем, что для пустого списка возвращается пустой список
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


def test_single_transaction():
    # Проверяем работу с одной транзакцией
    single_trans = [{"id": 100, "description": "Тестовая операция"}]
    descriptions = list(transaction_descriptions(single_trans))
    assert descriptions == ["Тестовая операция"]


# Для третьей функции
# Тесты для проверки форматирования одиночных значений
@pytest.mark.parametrize(
    "number, expected",
    [
        (1, "0000 0000 0000 0001"),
        (123, "0000 0000 0000 0123"),
        (123456789, "0000 0001 2345 6789"),
        (9999999999999999, "9999 9999 9999 9999"),
    ],
)
def test_single_card_format(number, expected):
    result = list(card_number_generator(number, number))
    assert result == [expected]


# Тесты для проверки диапазонов и количества элементов
@pytest.mark.parametrize(
    "start, end, expected_count, first_expected, last_expected",
    [
        (1, 5, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        # Исправлено: ожидаемый результат теперь верный
        (123456789, 123456791, 3, "0000 0001 2345 6789", "0000 0001 2345 6791"),
    ],
)
def test_card_range(start, end, expected_count, first_expected, last_expected):
    result = list(card_number_generator(start, end))
    assert len(result) == expected_count
    assert result[0] == first_expected
    assert result[-1] == last_expected


# Тесты для граничных случаев
def test_empty_range():
    # Если start > end, диапазон пуст
    result = list(card_number_generator(5, 1))
    assert result == []


def test_zero_and_one():
    # Проверка генерации с нуля и единицы
    result = list(card_number_generator(1, 2))
    assert result == ["0000 0000 0000 0001", "0000 0000 0000 0002"]
