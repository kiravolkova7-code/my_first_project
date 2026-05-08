import pytest
from src.widget import mask_account_card, get_date


# Для первой функции
def test_mask_card() -> None:
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"


def test_mask_account() -> None:
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


@pytest.mark.parametrize("input_str, expected", [
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ("Мир 9876543210987654", "Мир 9876 54** **** 7654"),
    ("Счет 1111222233334444", "Счет **4444"),
    ("Счет 0000111122223333", "Счет **3333"),
])
def test_parametrized(input_str: str, expected: str) -> None:
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("invalid_input", [
    "",                          # пустая строка
    "1234567890",                # только номер, без типа
    "Некорректный тип 1234",     # неизвестный тип
    "Счет",                      # только тип, без номера
    "Счет abcdefg",              # нечисловой номер
])
def test_invalid_inputs(invalid_input: str) -> None:
    with pytest.raises(Exception):
        mask_account_card(invalid_input)


# Для второй функции
def test_valid_date_conversion() -> None:
    input_date = "2024-03-11T02:26:18.671407"
    expected = "11.03.2024"
    assert get_date(input_date) == expected


@pytest.mark.parametrize("input_str, expected", [
    ("2000-01-01T00:00:00.000000", "01.01.2000"),   # Граница веков
    ("1999-12-31T23:59:59.999999", "31.12.1999"),   # Конец года
    ("2024-02-29T12:34:56.789012", "29.02.2024"),   # Високосный год
    ("2023-04-05T10:11:12.345678", "05.04.2023"),   # Обычная дата
])
def test_various_date_formats(input_str: str, expected: str) -> None:
    assert get_date(input_str) == expected
