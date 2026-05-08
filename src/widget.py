from src.masks import *

def mask_account_card(input_str: str) -> str:
    """
    Принимает строку вида 'Visa Platinum 7000792289606361' или 'Счет 73654108430135874305'
    и возвращает строку с замаскированным номером.
    """
    parts = input_str.split()
    # Последний элемент — номер, всё остальное — тип
    number = parts[-1]
    type_part = " ".join(parts[:-1])

    if type_part.lower().startswith("счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{type_part} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой из формата "2024-03-11T02:26:18.671407"
    в формат "ДД.ММ.ГГГГ" (например, "11.03.2024").
    """
    # Проверка на None или нестроковый тип
    if not isinstance(date_str, str):
        raise ValueError("Некорректный формат даты")

    try:
        # Разделяем строку по 'T'
        date_part = date_part = date_str.split("T")[0]

        # Проверяем, что в части до T есть два дефиса
        if date_part.count("-") != 2:
            raise ValueError

        year, month, day = date_part.split("-")

        # Простая проверка на числовые значения (можно сделать строже)
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError

        return f"{day}.{month}.{year}"

    except (IndexError, ValueError):
        raise ValueError("Некорректный формат даты")

