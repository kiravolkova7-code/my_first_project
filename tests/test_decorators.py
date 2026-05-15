import pytest
import os
from src.decorators import log


# Фикстура для очистки лог-файла перед и после тестов
@pytest.fixture
def cleanup_logfile():
    filename = "test_log.txt"
    # Удаляем файл, если он существует перед тестом
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    # Удаляем файл после теста
    if os.path.exists(filename):
        os.remove(filename)


# 1. Тест: Логирование в консоль при успешном выполнении
def test_log_success_console(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)

    captured = capsys.readouterr()
    # Проверяем результат функции
    assert result == 5
    # Проверяем вывод в консоль (имя функции может быть 'add' или 'test_log_success_console.<locals>.add')
    assert "ok" in captured.out
    assert "add" in captured.out or "test_log_success_console.<locals>.add" in captured.out


# 2. Тест: Логирование в файл при успешном выполнении
def test_log_success_file(cleanup_logfile):
    filename = cleanup_logfile

    @log(filename=filename)
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)

    # Проверяем результат функции
    assert result == 20
    # Проверяем содержимое файла
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "multiply ok" in content or "test_log_success_file.<locals>.multiply ok" in content


# 3. Тест: Логирование ошибки в консоль
def test_log_error_console(capsys):
    @log()
    def divide(a, b):
        return a / b  # Вызовет ZeroDivisionError

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out


# 4. Тест: Логирование ошибки в файл
def test_log_error_file(cleanup_logfile):
    filename = cleanup_logfile

    @log(filename=filename)
    def failing_func(x):
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_func(42)

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "error: ValueError" in content
        assert "Inputs: (42,), {}" in content


# 5. Тест: Проверка передачи ключевых аргументов при ошибке
def test_log_kwargs_error(capsys):
    @log()
    def func_with_kwargs(a, option=True):
        if not option:
            raise RuntimeError("Option is False")
        return a

    with pytest.raises(RuntimeError):
        func_with_kwargs(100, option=False)

    captured = capsys.readouterr()
    assert "error: RuntimeError" in captured.out
    assert "Inputs: (100,)" in captured.out and "{'option': False}" in captured.out
