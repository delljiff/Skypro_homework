from typing import List, Tuple

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Базовый тест для функции get_mask_card_number
def test_get_mask_card_number() -> None:
    assert get_mask_card_number("4967396863956970") == "4967 39** **** 6970"


# Базовый тест для функции get_mask_card_number с неверными данными
def test_get_mask_card_number_with_invalid_data() -> None:
    assert get_mask_card_number("496ха9686ував970") == "Вы неверно ввели номер карты"
    assert get_mask_card_number("496739686395697056557") == "Вы неверно ввели номер карты"
    assert get_mask_card_number("4967 3968") == "Вы неверно ввели номер карты"


# Базовый тест для функции get_mask_card_number с пустыми данными
def test_get_mask_card_number_with_no_data() -> None:
    assert get_mask_card_number("") == "Вы неверно ввели номер карты"


# Фикстура для создания тестовых данных для функции get_mask_card_number
@pytest.fixture
def data_for_input() -> List[Tuple[str, str]]:
    return [
        ("4967396863956970", "4967 39** **** 6970"),
        ("496ха9686ував970", "Вы неверно ввели номер карты"),
        ("496739686395697056557", "Вы неверно ввели номер карты"),
        ("4967 3968", "Вы неверно ввели номер карты"),
        ("", "Вы неверно ввели номер карты")
    ]


# Проверка работоспособности с фикстурой для функции get_mask_card_number
def test_with_fixture(data_for_input: List[Tuple[str, str]]) -> None:
    for card_number, expected in data_for_input:
        result = get_mask_card_number(card_number)
        assert result == expected


# Проверка работоспособности с параметризацией
@pytest.mark.parametrize(
    "card_data, expected",
    [
        ("4967396863956970", "4967 39** **** 6970"),
        ("496ха9686ував970", "Вы неверно ввели номер карты"),
        ("496739686395697056557", "Вы неверно ввели номер карты"),
        ("4967 3968", "Вы неверно ввели номер карты"),
        ("", "Вы неверно ввели номер карты")
    ]
)


# Проверка раотоспособности с параметризацией get_mask_card_number
def test_with_parametrize(card_data: str, expected: str) -> None:
    assert get_mask_card_number(card_data) == expected


# Базовый тест для функции get_mask_account
def test_get_mask_account() -> None:
    assert get_mask_account("73654108430135874305") == "**4305"


# Базовый тест для функции get_mask_account с неверными данными
def test_get_mask_account_with_invalid_data() -> None:
    assert get_mask_account("7365svgf430ee58gkvnd") == "Вы неверно ввели номер счета"
    assert get_mask_account("736556") == "Вы неверно ввели номер счета"


# Базовый тест для функции get_mask_account с пустыми данными
def test_get_mask_account_with_no_data() -> None:
    assert get_mask_account("") == "Вы неверно ввели номер счета"


# Фикстура для создания тестовых данных для функции get_mask_account
@pytest.fixture
def data_for_input_2() -> List[Tuple[str, str]]:
    return [
        ("73654108430135874305", "**4305"),
        ("7365svgf430ee58gkvnd", "Вы неверно ввели номер счета"),
        ("736556", "Вы неверно ввели номер счета"),
        ("", "Вы неверно ввели номер счета")
    ]


# Проверка работоспособности с фикстурой для функции get_mask_account
def test_with_fixture_2(data_for_input_2: List[Tuple[str, str]]) -> None:
    for account_number, expected in data_for_input_2:
        result = get_mask_account(account_number)
        assert result == expected


# Проверка работоспособности с параметризацией
@pytest.mark.parametrize(
    "account_data, expected",
    [
        ("73654108430135874305", "**4305"),
        ("7365svgf430ee58gkvnd", "Вы неверно ввели номер счета"),
        ("736556", "Вы неверно ввели номер счета"),
        ("", "Вы неверно ввели номер счета")
    ]
)


# Проверка работоспособности с параметризацией get_mask_account
def test_with_parametrize_2(account_data: str, expected: str) -> None:
    assert get_mask_account(account_data) == expected
