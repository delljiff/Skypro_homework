import json
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_transactions_with_mock() -> None:
    """Тест: загрузка транзакций через mock (без реального файла)"""
    mock_data: List[Dict[str, Any]] = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]

    with patch("src.utils.os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result: List[Dict[str, Any]] = load_transactions("fake_path.json")

    assert result == mock_data
    assert len(result) == 2


def test_load_transactions_file_not_found() -> None:
    """Тест: файл не найден → пустой список"""
    with patch("src.utils.os.path.exists", return_value=False):
        result: List[Dict[str, Any]] = load_transactions("nonexistent.json")
    assert result == []


def test_load_transactions_invalid_json() -> None:
    """Тест: невалидный JSON → пустой список"""
    with patch("src.utils.os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="{invalid json}")):
            result: List[Dict[str, Any]] = load_transactions("fake.json")
    assert result == []


def test_load_transactions_not_list() -> None:
    """Тест: данные не список → пустой список"""
    with patch("src.utils.os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            result: List[Dict[str, Any]] = load_transactions("fake.json")
    assert result == []
