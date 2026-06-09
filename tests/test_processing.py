from src.processing import filter_by_state, sort_by_date

# Тип для одного элемента в списке, чтобы избежать повторений
ItemType = Dict[str, Optional[str]]


# Для первой функции
def test_filter_by_state_default(test_items: List[ItemType]) -> None:
    result = filter_by_state(test_items)
    assert len(result) == 3
    assert all(item["state"] == "EXECUTED" for item in result)


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 3),
    ("PENDING", 1),
    ("FAILED", 1),
    ("UNKNOWN", 0),
    (None, 1),
])
def test_filter_by_state_parametrized(
    test_items: List[ItemType],
    state: Optional[str],
    expected_count: int
) -> None:
    result = filter_by_state(test_items, state=state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(item["state"] == state for item in result)


# Для второй функции
def test_sort_by_date_descending(test_items: List[ItemType]) -> None:
    result = sort_by_date(test_items, descending=True)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(test_items: List[ItemType]) -> None:
    result = sort_by_date(test_items, descending=False)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates)


def test_sort_by_date_same_dates() -> None:
    items: List[ItemType] = [
        {"id": "1", "date": "2023-10-01T12:00:00"},
        {"id": "2", "date": "2023-10-01T12:00:00"},
        {"id": "3", "date": "2023-10-01T12:00:00"},
    ]
    result = sort_by_date(items)
    assert [item["id"] for item in result] == ["1", "2", "3"]


def test_sort_by_date_invalid_format() -> None:
    items: List[ItemType] = [
        {"id": "1", "date": "invalid-date"},
        {"id": "2", "date": "2023-10-01T12:00:00"},
    ]
    result = sort_by_date(items)
    assert len(result) == len(items)
