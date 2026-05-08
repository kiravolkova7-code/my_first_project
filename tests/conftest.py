import pytest
from typing import List, Dict, Optional


@pytest.fixture
def test_items() -> List[Dict[str, Optional[str]]]:
    return [
        {"id": "1", "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": "2", "state": "PENDING",  "date": "2023-10-02T12:00:00"},
        {"id": "3", "state": "EXECUTED", "date": "2023-10-03T12:00:00"},
        {"id": "4", "state": "FAILED",   "date": "2023-10-04T12:00:00"},
        {"id": "5", "state": None,       "date": "2023-10-05T12:00:00"},
        {"id": "6", "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
    ]
