import logging

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
    except Exception as e:
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
    except Exception as e:
        logging.exception("Ошибка при маскировке номера счёта")
        raise