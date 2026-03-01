from typing import List, Tuple

import pytest

from src.widget import get_date, mask_account_card


# Базовый тест для функции mask_account_card
def test_mask_account_card() -> None:
    assert mask_account_card("Visa Platinum 1234567890123456") == "Visa Platinum 1234 56** **** 3456"
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"


# Базовый тест для функции mask_account_card с неверными данными
def test_mask_account_card_with_invalid_data() -> None:
    assert mask_account_card("Visa 1234") == "Неверно введены данные"
    assert mask_account_card("Счет 12345") == "Неверно введены данные"
    assert mask_account_card("MasterCard abcd1234efgh5678") == "Неверно введены данные"
    assert mask_account_card("Visa 12345678901234567") == "Неверно введены данные"
    assert mask_account_card("1234567890123456") == "Неверно введены данные"
    assert mask_account_card("Счет") == "Неверно введены данные"


# Базовый тест для функции mask_account_card с пустыми данными
def test_mask_account_card_with_no_data() -> None:
    assert mask_account_card("") == "Неверно введены данные"


# Фикстура для создания тестовых данных для функции mask_account_card
@pytest.fixture
def data_for_input_3() -> List[Tuple[str, str]]:
    return [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Visa 1234", "Неверно введены данные"),
        ("Счет 12345", "Неверно введены данные"),
        ("MasterCard abcd1234efgh5678", "Неверно введены данные"),
        ("Visa 12345678901234567", "Неверно введены данные"),
        ("1234567890123456", "Неверно введены данные"),
        ("Счет", "Неверно введены данные"),
        ("", "Неверно введены данные"),
    ]


# Проверка работоспособности с фикстурой для функции mask_account_card
def test_mask_account_card_with_fixture(data_for_input_3: List[Tuple[str, str]]) -> None:
    for card_or_acc_data, expected in data_for_input_3:
        assert mask_account_card(card_or_acc_data) == expected


# Проверка работоспособности с параметризацией
@pytest.mark.parametrize(
    "card_acc_data, expected",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
        ("Maestro 5555666677778888", "Maestro 5555 66** **** 8888"),
        ("Visa Classic 1111222233334444", "Visa Classic 1111 22** **** 4444"),
        ("American Express 1234567890123456", "American Express 1234 56** **** 3456"),
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("МИР 1234123412341234", "МИР 1234 12** **** 1234"),
        ("Visa 1234", "Неверно введены данные"),
        ("Счет 12345", "Неверно введены данные"),
        ("MasterCard abcd1234efgh5678", "Неверно введены данные"),
        ("Visa 12345678901234567", "Неверно введены данные"),
        ("1234567890123456", "Неверно введены данные"),
        ("Счет", "Неверно введены данные"),
        ("", "Неверно введены данные"),
    ],
)


# Проверка работоспособности с параметризацией mask_account_card
def test_with_parametrize_3(card_acc_data: str, expected: str) -> None:
    assert mask_account_card(card_acc_data) == expected


# Базовый тест для функции get_date (в разных вариациях)
def test_get_date() -> None:
    assert get_date("2024-03-15T10:30:00") == "15.03.2024"
    assert get_date("2024-03-15") == "15.03.2024"
    assert get_date("2024-03-15 10:30:00") == "15.03.2024"
    assert get_date("2023-12-31T23:59:59") == "31.12.2023"
    assert get_date("2024-01-01T00:00:00") == "01.01.2024"
    assert get_date("2024-02-29T12:00:00") == "29.02.2024"


# Базовый тест для функции get_date (с необычным вводом)
def test_get_date_with_invalid_data() -> None:
    assert get_date("") == "Неверный формат даты"
    assert get_date("2024") == "Неверный формат даты"
    assert get_date("2024-03") == "Неверный формат даты"
    assert get_date("15.03.2024") == "Неверный формат даты"
    assert get_date("hello world") == "Неверный формат даты"
    assert get_date("12345") == "Неверный формат даты"
    assert get_date("@#$%^&*()") == "Неверный формат даты"


# Фикстура для создания тестовых данных для функции get_date
@pytest.fixture
def data_for_input_4() -> List[Tuple[str, str]]:
    return [
        ("2024-03-15T10:30:00", "15.03.2024"),
        ("2024-03-15", "15.03.2024"),
        ("2024-03-15 10:30:00", "15.03.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-02-29T12:00:00", "29.02.2024"),
        ("", "Неверный формат даты"),
        ("2024", "Неверный формат даты"),
        ("2024-03", "Неверный формат даты"),
        ("15.03.2024", "Неверный формат даты"),
        ("hello world", "Неверный формат даты"),
        ("12345", "Неверный формат даты"),
        ("@#$%^&*()", "Неверный формат даты"),
    ]


# Проверка работоспособности с фикстурой для функции get_date
def test_get_date_with_fixture(data_for_input_4: List[Tuple[str, str]]) -> None:
    for unformatted_date, expected in data_for_input_4:
        assert get_date(unformatted_date) == expected


# Проверка работоспособности с параметризацией
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-15T10:30:00", "15.03.2024"),
        ("2024-03-15", "15.03.2024"),
        ("2024-03-15 10:30:00", "15.03.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-02-29T12:00:00", "29.02.2024"),
        ("", "Неверный формат даты"),
        ("2024", "Неверный формат даты"),
        ("2024-03", "Неверный формат даты"),
        ("15.03.2024", "Неверный формат даты"),
        ("hello world", "Неверный формат даты"),
        ("12345", "Неверный формат даты"),
        ("@#$%^&*()", "Неверный формат даты"),
    ],
)


# Проверка работоспособности с параметризацией get_date
def test_with_parametrize_4(input_date: str, expected: str) -> None:
    assert get_date(input_date) == expected
