from src.utils import load_operations


def test_load_valid_json(mocker):
    """
    Проверяет, что функция корректно загружает валидный JSON-список.
    """
    # 1. Подменяем проверку существования файла
    mocker.patch('os.path.exists', return_value=True)

    # 2. Подменяем открытие файла и его содержимое
    mock_file = mocker.mock_open(read_data='[{"amount": 100, "currency": "USD"}]')
    mocker.patch('builtins.open', mock_file)

    # 3. Вызываем функцию и проверяем результат
    result = load_operations('test.json')
    assert result == [{"amount": 100, "currency": "USD"}]


def test_file_not_found(mocker):
    """
    Проверяет, что функция возвращает пустой список, если файл не найден.
    """

    mocker.patch('os.path.exists', return_value=False)

    result = load_operations('missing.json')
    assert result == []


def test_invalid_json(mocker):
    """
    Проверяет обработку некорректного JSON-контента.
    """
    mocker.patch('os.path.exists', return_value=True)

    # Подставляем невалидный JSON
    mocker.patch('builtins.open', mocker.mock_open(read_data='{invalid json}'))

    result = load_operations('test.json')
    assert result == []
