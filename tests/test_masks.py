import pytest
from src.masks import get_mask_card_number, get_mask_account

# Для первой функции
def test_valid_card_number():
    # Стандартный валидный номер карты
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

def test_card_number_with_spaces():
    # Номер карты с пробелами
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"

def test_card_number_with_leading_zeros():
    # Номер карты с ведущими нулями
    assert get_mask_card_number("0000111122223333") == "0000 11** **** 3333"

def test_invalid_length_card_number():
    # Номер карты короче 16 цифр
    with pytest.raises(ValueError):
        get_mask_card_number("123456789012345")

def test_invalid_length_long_card_number():
    # Номер карты длиннее 16 цифр
    with pytest.raises(ValueError):
        get_mask_card_number("123456789012345678")

def test_empty_string():
    # Пустая строка
    with pytest.raises(ValueError):
        get_mask_card_number("")

# Для второй функции
@pytest.mark.parametrize('number, res', [
    ("1234567890", "**7890"),
    ("00001234", "**1234"),
    ("987654321", "**4321")
])
def test_masking_correct(number, res):
    assert get_mask_account(number) == res


def test_various_formats_and_lengths():
    # Минимально допустимая длина (4 цифры)
    assert get_mask_account("1234") == "**1234"
    # Длинный номер счёта
    assert get_mask_account("12345678901234567890") == "**7890"
    # Номер счёта с пробелами
    assert get_mask_account("12 34 56 78 90") == "**7890"


def test_error_handling():
    # Слишком короткий номер (3 цифры)
    with pytest.raises(ValueError):
        get_mask_account("123")
    # Пустой ввод
    with pytest.raises(ValueError):
        get_mask_account("")
    # Номер с буквами (не только цифры)
    with pytest.raises(ValueError):
        get_mask_account("12a4")