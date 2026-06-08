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
    # Поиск строчными буквами должен найти оба варианта
    result_lower = process_bank_search(data, "кафе")
    assert len(result_lower) == 2

    # Поиск заглавными буквами также должен быть успешным
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
    Такие записи должны игнорироваться.
    """
    data = [
        {"id": 1, "amount": 500},
        {"id": 2, "description": "Найдено!", "amount": 100}
    ]
    result = process_bank_search(data, "найд")
    # В результате должна быть только вторая запись
    assert result == [data[1]]

# Тесты для второй функции счетчика
@pytest.fixture
def sample_data() -> List[Dict]:
    """Фикстура, предоставляющая образец данных для большинства тестов."""
    return [
        {"id": 1, "amount": 500, "description": "Оплата за продукты в Пятёрочке"},
        {"id": 2, "amount": 300, "description": "Такси до дома"},
        {"id": 3, "amount": 1500, "description": "Зарплата за месяц"},
        {"id": 4, "amount": 200, "description": "Кафе на Арбате"},
        {"id": 5, "amount": 100, "description": "Продукты и бытовая химия"},
        {"id": 6, "amount": 50,  "description": "проезд на метро"}, # Проверка регистра
    ]


def test_basic_counting(sample_data):
    """Проверяет корректный подсчёт нескольких категорий."""
    categories = ["продукты", "такси"]
    expected_result = {"продукты": 2, "такси": 1}
    assert process_bank_operations(sample_data, categories) == expected_result


def test_case_insensitivity(sample_data):
    """Проверяет, что поиск не зависит от регистра символов."""
    categories = ["ПРОДУКТЫ", "МЕТРО"] # Категории в верхнем регистре
    expected_result = {"ПРОДУКТЫ": 2, "МЕТРО": 1} # Должны найти записи с любым регистром
    assert process_bank_operations(sample_data, categories) == expected_result


def test_empty_data_list():
    """Проверяет работу функции с пустым списком данных."""
    empty_data: List[Dict] = []
    categories = ["продукты"]
    expected_result = {"продукты": 0}
    assert process_bank_operations(empty_data, categories) == expected_result


def test_multiple_matches_in_one_desc():
    """Проверяет, что несколько совпадений в одном описании считаются правильно."""
    data = [
        {
            "id": 1,
            "description": "Купил продукты (молоко, хлеб) и поехал на такси домой."
        }
    ]
    categories = ["продукты", "такси"]
    expected_result = {"продукты": 1, "такси": 1}
    assert process_bank_operations(data, categories) == expected_result