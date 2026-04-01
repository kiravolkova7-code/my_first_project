def get_mask_card_number(card_number: str) -> str:
    # Убираем пробелы, если они есть
    card_number = card_number.replace(" ", "")

    # Проверяем, что номер карты состоит только из цифр и имеет длину 16
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр")


    # Формируем маску: первые 6 цифр, затем две звезды, затем 4 звезды, затем последние 4 цифры
    masked = (
        card_number[:4]
        + " "
        + card_number[4:6]
        + "**"
        + " "
        + "****"
        + " "
        + card_number[-4:]
    )
    return masked


def get_mask_account(account_number: str) -> str:
    # Убираем пробелы, если они есть
    account_number = account_number.replace(" ", "")

    # Проверяем, что номер счёта состоит только из цифр и имеет длину не менее 4
    if not account_number.isdigit() or len(account_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    # Формируем маску: две звезды и последние 4 цифры
    masked = "**" + account_number[-4:]
    return masked
