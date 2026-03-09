from typing import Any, Dict, Generator, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тесты для filter_by_currency
@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями"""
    return [
        {"id": 1, "currency": "USD", "description": "Покупка в Amazon", "amount": 100.50},
        {"id": 2, "currency": "EUR", "description": "Кафе в Берлине", "amount": 25.30},
        {"id": 3, "currency": "USD", "description": "Подписка Netflix", "amount": 15.99},
        {"id": 4, "currency": "RUB", "description": "Пятерочка", "amount": 1500.00},
    ]


@pytest.mark.parametrize(
    "currency, expected_count, expected_ids",
    [
        ("USD", 2, [1, 3]),  # Долларовые транзакции
        ("EUR", 1, [2]),  # Транзакции в евро
        ("RUB", 1, [4]),  # Транзакции в рублях
        ("GBP", 0, []),  # Нет транзакций в фунтах
    ],
)
def test_filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str, expected_count: int, expected_ids: List[int]
) -> None:
    """Проверяет фильтрацию транзакций по валюте"""
    filtered_gen: Generator[Dict[str, Any], None, None] = filter_by_currency(transactions, currency)
    result: List[Dict[str, Any]] = list(filtered_gen)

    assert len(result) == expected_count
    assert [t["id"] for t in result] == expected_ids


def test_filter_by_currency_empty() -> None:
    """Проверяет обработку пустого списка"""
    empty_list: List[Dict[str, Any]] = []
    result: List[Dict[str, Any]] = list(filter_by_currency(empty_list, "USD"))
    assert result == []


# Тесты для transaction_descriptions
@pytest.fixture
def transactions_with_desc() -> List[Dict[str, str]]:
    """Фикстура с транзакциями для описаний"""
    return [
        {"description": "Покупка в Amazon"},
        {"description": "Кафе в Берлине"},
        {"description": "Подписка Netflix"},
    ]


def test_transaction_descriptions(transactions_with_desc: List[Dict[str, str]]) -> None:
    """Проверяет извлечение описаний транзакций"""
    desc_gen: Generator[str, None, None] = transaction_descriptions(transactions_with_desc)
    result: List[str] = list(desc_gen)
    expected: List[str] = ["Покупка в Amazon", "Кафе в Берлине", "Подписка Netflix"]

    assert result == expected


def test_transaction_descriptions_empty() -> None:
    """Проверяет обработку пустого списка"""
    empty_list: List[Dict[str, str]] = []
    result: List[str] = list(transaction_descriptions(empty_list))
    assert result == []


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start, stop, expected_count, expected_first, expected_last",
    [
        (1, 3, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),  # Начало диапазона
        (9999, 10001, 3, "0000 0000 0000 9999", "0000 0000 0001 0001"),  # Переход через разряд
    ],
)
def test_card_number_generator(
    start: int, stop: int, expected_count: int, expected_first: str, expected_last: str
) -> None:
    """Проверяет генерацию номеров карт в диапазоне"""
    card_gen: Generator[str, None, None] = card_number_generator(start, stop)
    result: List[str] = list(card_gen)

    assert len(result) == expected_count
    assert result[0] == expected_first
    assert result[-1] == expected_last


def test_card_number_generator_single() -> None:
    """Проверяет генерацию одного номера"""
    result: List[str] = list(card_number_generator(5, 5))
    assert result == ["0000 0000 0000 0005"]


def test_card_number_generator_format() -> None:
    """Проверяет форматирование номера карты"""
    result: List[str] = list(card_number_generator(12345678, 12345678))

    assert result[0] is not None
    assert len(result[0]) == 19  # 16 цифр + 3 пробела

    parts: List[str] = result[0].split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
