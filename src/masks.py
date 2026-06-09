import logging
import re

# Настройка логгера: файл перезаписывается при каждом запуске
logging.basicConfig(
    filename='logs/app_masks.log',
    level=logging.INFO,
    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
    filemode='w',
    encoding='utf-8'
)


def get_mask_card_number(card_number: str) -> str:
    try:
        logging.info(f"Попытка маскировки номера карты: {card_number}")
        card_number = card_number.replace(" ", "")
        if len(card_number) != 16:
            logging.error("Неверная длина номера карты (ожидалось 16 цифр)")
            raise ValueError("Номер карты должен содержать ровно 16 цифр")
        masked = (
            card_number[:4] + " " +
            card_number[4:6] + "**" + " " +
            "****" + " " +
            card_number[-4:]
        )
        logging.info(f"Номер карты успешно замаскирован: {masked}")
        return masked
    except Exception:
        logging.exception("Ошибка при маскировке номера карты")
        raise


def get_mask_account(account_number: str) -> str:
    try:
        logging.info(f"Попытка маскировки номера счёта: {account_number}")
        account_number = account_number.replace(" ", "")
        if not account_number.isdigit() or len(account_number) < 4:
            logging.error("Неверный формат или длина номера счёта")
            raise ValueError("Номер счёта должен содержать минимум 4 цифры")
        masked = "**" + account_number[-4:]
        logging.info(f"Номер счёта успешно замаскирован: {masked}")
        return masked
    except Exception:
        logging.exception("Ошибка при маскировке номера счёта")
        raise


def mask_requisite(requisite_str):
    """
    Определяет тип реквизита (карта или счет) и применяет соответствующую маску.
    """
    if not isinstance(requisite_str, str):
        return requisite_str

    # Проверяем, начинается ли строка с "Счет " (с учетом регистра)
    if re.match(r'^Счет\s', requisite_str):
        digits = re.sub(r'\D', '', requisite_str)
        try:
            masked_digits = get_mask_account(digits)
            return f"Счет {masked_digits}"
        except (ValueError, TypeError):
            return requisite_str

    # Ищем строку, где есть слово, за которым идут не-цифры, а затем 16 цифр.
    card_match = re.search(r'(\b\w+\b[ \w-]*)\D+(\d{16})', requisite_str, re.IGNORECASE)
    if card_match:
        # Группа 1: Название карты (например, "Visa Classic")
        card_name = card_match.group(1).strip()
        # Группа 2: Номер карты (16 цифр)
        card_digits = card_match.group(2)

        try:
            masked_digits = get_mask_card_number(card_digits)
            return f"{card_name} {masked_digits}"
        except ValueError:
            return requisite_str

    # Если тип определить не удалось, возвращаем строку без изменений
    return requisite_str
