import pytest
from typing import List, Dict
from src.search_prosessing import process_bank_search, process_bank_operations

# Тесты для первой функции поиска
def test_basic_search():
    """Проверяет базовый поиск по подстроке."""
    data = [
        {"id": 1, "description": "Покупка продуктов"},
        {"id": 2, "description": "Оплата интернета"},
        {"id": 3, "description": "Снятие наличных"}
    ]
    search_query = "продукт"
    expected = [data[0]]
    result = process_bank_search(data, search_query)
    assert result == expected


def test_case_insensitive_search():
    """Проверяет, что поиск не зависит от регистра символов."""
    data = [
        {"id": 1, "description": "Кафе на Арбате"},
        {"id": 2, "description": "КАФЕ у дома"},
        {"id": 3, "description": "Обед в ресторане"}
    ]

    result_lower = process_bank_search(data, "кафе")
    assert len(result_lower) == 2

    result_upper = process_bank_search(data, "КАФЕ")
    assert len(result_upper) == 2


def test_empty_data_list():
    """Проверяет работу функции с пустым списком данных."""
    data: List[Dict] = []
    result = process_bank_search(data, "поиск")
    assert result == []


def test_missing_description_key():
    """
    Проверяет, что функция корректно обрабатывает словари,
    в которых отсутствует ключ 'description'.
    """
    data = [
        {"id": 1, "amount": 500},
        {"id": 2, "description": "Найдено!", "amount": 100}
    ]
    result = process_bank_search(data, "найд")

    assert result == [data[1]]

# Тесты для второй функции счетчика
def test_empty_result_with_categories():
    """
    Проверяет, что если данные есть, а совпадений нет,
    возвращаются нули для всех переданных категорий.
    """
    data = [{"description": "Случайный текст без категорий"}]
    categories = ["Еда", "Транспорт"]

    result = process_bank_operations(data, categories)
    assert result == {"Еда": 0, "Транспорт": 0}


def test_returns_zero_for_missing_category():
    """
    Проверяет, что функция возвращает 0 для категории,
    которая есть в списке, но не встречается в данных.
    """
    data = [
        {"description": "Купил Продукт"},
        {"description": "Оплата ЖКХ"}
    ]
    categories = ["Продукт", "ЖКХ", "Развлечения"]

    result = process_bank_operations(data, categories)

    assert result == {"Продукт": 1, "ЖКХ": 1, "Развлечения": 0}


def test_partial_match_and_word_boundaries():
    """
    Проверяет поиск подстроки (например, 'Кредит' в 'кредитную').
    """
    data = [
        {"description": "Перевод за кредитную карту"},
        {"description": "Подписка на телеграм-канал Кредитка"}
    ]
    categories = ["Кредит"]

    result = process_bank_operations(data, categories)

    assert result == {"Кредит": 2}


