import functools
import datetime


def log(filename=None):
    """
    Декоратор для логирования выполнения функции.
    Записывает в лог успешное выполнение функции или информацию о возникшем исключении.
    Каждое сообщение лога снабжается временной меткой.
    Args: filename (str, optional): Путь к файлу, в который будут
    записываться логи.
    Если аргумент не указан (None), логи выводятся в стандартный поток вывода (stdout).
    Returns: function: Декоратор, который оборачивает целевую функцию.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result
            except Exception as e:
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(error_message, filename)
                raise  # Перебрасываем ошибку дальше
        return wrapper
    return decorator


def _write_log(message, filename):
    """
    Записывает сообщение лога в файл или выводит его в стандартный поток вывода.
    К сообщению добавляется временная метка в формате 'YYYY-MM-DD HH:MM:SS'.
    Args: message (str): Текст сообщения для лога.
    filename (str или None): Имя файла для записи. Если None, сообщение выводится в stdout.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    else:
        print(log_entry, end='')
