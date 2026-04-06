from typing import Any, Dict
from unittest.mock import Mock, patch

from src.external_api import convert_to_rub


def test_convert_to_rub_rub() -> None:
    """Тест: если валюта RUB, возвращается сумма без API"""
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
        "date": "2020-01-01T00:00:00",
    }
    result: float = convert_to_rub(transaction)
    assert result == 100.0


def test_convert_to_rub_usd() -> None:
    """Тест: USD конвертируется через API (используем mock)"""
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
        "date": "2020-01-01T00:00:00",
    }

    mock_response: Mock = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.5}}

    with patch("src.external_api.requests.get", return_value=mock_response):
        result: float = convert_to_rub(transaction)

    assert result == 7550.0
