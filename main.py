import sys
import re
from datetime import datetime
from src.reader_csv_xlsx import read_transactions_csv, read_transactions_excel
from src.utils import load_operations
from src.masks import get_mask_card_number, get_mask_account, mask_requisite


def main():
    """Основная функция программы для работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # 1. Выбор формата файла и получение пути к нему
    file_type = input("Ваш выбор: ").strip()
    file_options = {
        '1': (load_operations, "JSON", "data/operations.json"),
        '2': (read_transactions_csv, "CSV", "data/transactions.csv"),
        '3': (read_transactions_excel, "XLSX", "data/transactions_excel.xlsx")
    }

    if file_type not in file_options:
        print("Неверный выбор. Программа завершает работу.")
        return

    reader_func, file_type_name, file_path = file_options[file_type]
    print(f"Для обработки выбран {file_type_name}-файл по пути '{file_path}'.")

    # 3. Чтение данных из файла с обработкой ошибок
    try:
        transactions = reader_func(file_path)
        if not transactions:
            print("Файл не содержит транзакций или не удалось их прочитать.")
            return

        # --- ОТЛАДКА: СКОЛЬКО ДАННЫХ МЫ СЧИТАЛИ? ---
        print(f"[ОТЛАДКА] Считано всего транзакций из файла: {len(transactions)}")
        # -------------------------------------------

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return

    # 4. Фильтрация по статусу
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        status_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            "Ваш выбор: "
        ).strip().upper()
        if status_input in valid_statuses:
            # Используем более надежный способ сравнения
            filtered_by_status = [t for t in transactions if str(t.get('state', '')).strip().upper() == status_input]

            # --- ОТЛАДКА: СКОЛЬКО ТРАНЗАКЦИЙ ПРОШЛО ФИЛЬТРАЦИЮ? ---
            print(f"[ОТЛАДКА] После фильтрации по статусу '{status_input}' осталось: {len(filtered_by_status)}")
            # ----------------------------------------------------

            if not filtered_by_status:
                # Если после первой же фильтрации список пуст, выходим
                print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
                return

            print(f'Операции отфильтрованы по статусу "{status_input}"')
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    current_list = filtered_by_status

    # 5. Сортировка по дате
    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice in ["да", "yes", "y"]:
        order_choice = input(
            "Отсортировать по возрастанию или по убыванию? "
            "(введите 'возрастанию' или 'убыванию'): "
        ).strip().lower()
        reverse_order = order_choice == "убыванию"
        try:
            current_list = sorted(current_list, key=lambda t: t['date'], reverse=reverse_order)
            order_text = "убыванию" if reverse_order else "возрастанию"
            print(f"Список отсортирован по дате по {order_text}.")
        except (KeyError, TypeError) as e:
            # --- ОТЛАДКА: ПОЧЕМУ НЕ СОРТИРУЕТСЯ? ---
            print(f"[ОТЛАДКА] Ошибка при сортировке (возможно, нет ключа 'date' или неверный формат): {e}")
            # Мы не прерываем программу, а продолжаем с неотсортированным списком
            pass

    # 6. Фильтрация по валюте (рубли)
    currency_choice = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if currency_choice in ["да", "yes", "y"]:
        # Получаем вложенный словарь с валютой для каждой транзакции
        # Если структура нарушена, используем пустой словарь, чтобы избежать ошибок
        current_list = [
            t for t in current_list
            if t.get('operationAmount', {}).get('currency', {}).get('code') == "RUB"
        ]

        # --- ОТЛАДКА: СКОЛЬКО ОСТАЛОСЬ ПОСЛЕ ФИЛЬТРАЦИИ ПО ВАЛЮТЕ? ---
        print(f"[ОТЛАДКА] После фильтрации по валюте 'RUB' осталось: {len(current_list)}")
        # --------------------------------------------------------------
        print("Список отфильтрован: выводятся только рублевые транзакции.")

    # 7. Фильтрация по ключевому слову в описании
    keyword_choice = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if keyword_choice in ["да", "yes", "y"]:
        keyword = input("Введите ключевое слово для поиска в описании: ").strip().lower()
        current_list = [t for t in current_list if keyword in str(t.get('description', '')).lower()]
        # --- ОТЛАДКА: СКОЛЬКО ОСТАЛОСЬ ПОСЛЕ ПОИСКА ПО КЛЮЧЕВОМУ СЛОВУ? ---
        print(f"[ОТЛАДКА] После фильтрации по слову '{keyword}' осталось: {len(current_list)}")
        # -------------------------------------------------------------------
        print(f"Список отфильтрован: выводятся только транзакции, содержащие слово '{keyword}'.")

    # 8. Вывод итогового списка
    if not current_list:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print("\nРаспечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(current_list)}")
        for t in current_list:
            # --- УЛУЧШЕННАЯ ОБРАБОТКА ДАТЫ (БЕЗ ВНЕШНИХ БИБЛИОТЕК) ---
            date_value = t.get('date')
            date_str = "Дата не указана"
            if date_value and isinstance(date_value, str):
                try:
                    # Создаем копию строки, чтобы не изменять оригинал
                    date_str_for_parsing = date_value

                    # 1. Удаляем суффикс 'Z' (обозначает UTC), если он есть
                    if date_str_for_parsing.endswith('Z'):
                        date_str_for_parsing = date_str_for_parsing[:-1]

                    # 2. Удаляем микросекунды, если они есть
                    # Находим позицию первой точки
                    dot_pos = date_str_for_parsing.find('.')
                    if dot_pos != -1:
                        # Находим позицию символа 'T' (начало времени)
                        t_pos = date_str_for_parsing.find('T')
                        if t_pos != -1 and dot_pos > t_pos:
                            # Обрезаем строку до первого символа после времени, но до точки
                            date_str_for_parsing = date_str_for_parsing[:dot_pos]

                    # 3. Парсинг очищенной строки в объект datetime
                    # Теперь строка гарантированно в формате "%Y-%m-%dT%H:%M:%S"
                    date_obj = datetime.strptime(date_str_for_parsing, "%Y-%m-%dT%H:%M:%S")

                    # 4. Форматируем дату в нужный вид: 12.04.2019
                    date_str = date_obj.strftime("%d.%m.%Y")

                except (ValueError, TypeError, AttributeError):
                    # Если что-то пошло не так (не тот формат), оставляем строку по умолчанию
                    pass

            # Выводим результат (дату и описание)
            print(f"\n{date_str} {t.get('description', '')}")

            # --- ВЫВОД ИНФОРМАЦИИ О ТРАНЗАКЦИИ ---
            # 1. Описание и дата
            description = t.get('description', '')
            print(f"\n{date_str} {description}")

            # 2. Реквизиты (карта/счет) с маскировкой и обработкой ошибок
            from_value = t.get('from')
            to_value = t.get('to')

            if from_value and to_value:
                # Используем новую функцию для автоматической маскировки
                # Она сама определит тип и применит нужную маску
                masked_from = mask_requisite(from_value)
                masked_to = mask_requisite(to_value)

                print(f"{masked_from} -> {masked_to}")

            # 3. Сумма операции (учитываем вложенную структуру operationAmount)
            op_amount = t.get('operationAmount', {})
            amount = op_amount.get('amount')
            currency_obj = op_amount.get('currency', {})
            # Получаем название или код валюты
            currency_name = currency_obj.get('name') or currency_obj.get('code')

            if amount is not None and currency_name:
                print(f"Сумма: {amount} {currency_name}")

if __name__ == "__main__":
    main()