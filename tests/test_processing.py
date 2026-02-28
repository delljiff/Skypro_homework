import pytest

from typing import List, Dict, Any, Union

from src.processing import filter_by_state, sort_by_date


# Тестирование фильтрации списка словарей по заданному статусу state
def test_filter_by_state() -> None:
    data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "EXECUTED"}]

    result = filter_by_state(data, state="EXECUTED")

    assert result == [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]


# Проверка при отсутствии словарей с указанным статусом
def test_filter_by_state_no_status() -> None:
    data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]

    result = filter_by_state(data, state="CANCELED")

    assert result == []


# Фикстура с тестовыми данными
@pytest.fixture
def test_data() -> List[Dict]:
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4},
        {"status": "EXECUTED"},
        {},
    ]


def test_filter_by_state_executed(test_data: List[Dict[str, Any]]) -> None:
    result = filter_by_state(test_data, state="EXECUTED")
    assert result == [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]


def test_filter_by_state_canceled(test_data: List[Dict[str, Any]]) -> None:
    result = filter_by_state(test_data, state="CANCELED")
    assert result == [{"id": 2, "state": "CANCELED"}]


def test_filter_by_state_no_matching(test_data: List[Dict[str, Any]]) -> None:
    result = filter_by_state(test_data, state="COMPLETED")
    assert result == []


# Параметризация тестов для различных возможных значений статуса state
@pytest.mark.parametrize(
    "status, expected",
    [
        ("EXECUTED", [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]),
        ("CANCELED", [{"id": 2, "state": "CANCELED"}]),
        ("COMPLETED", []),
    ],
)
def test_filter_by_state_parametrized(status: str, expected: List[Dict]) -> None:
    data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "EXECUTED"}]

    result = filter_by_state(data, state=status)

    assert result == expected


# Одна фикстура со всеми данными для функции sort_by_date
@pytest.fixture
def data() -> List[List[Dict[str, Any]]]:
    return [
        # Для сортировки
        [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "2023-01-15"}, {"id": 3, "date": "2023-02-20"}],
        # С одинаковыми датами
        [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "2023-01-15"}, {"id": 3, "date": "2023-03-10"}],
        # С разными форматами
        [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "15.01.2023"}, {"id": 3, "date": "2023/02/20"}],
        # С некорректными данными
        [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "не дата"}, {"id": 3}, {"id": 4, "date": ""}],
        # Пустой список
        [],
    ]


# Сортировка по убыванию
def test_sort_desc(data: List[List[Dict[str, Any]]]) -> None:
    result = sort_by_date(data[0])
    assert [d["date"] for d in result] == ["2023-03-10", "2023-02-20", "2023-01-15"]


# Сортировка по возрастанию
def test_sort_asc(data: List[List[Dict[str, Any]]]) -> None:
    result = sort_by_date(data[0], reverse=False)
    assert [d["date"] for d in result] == ["2023-01-15", "2023-02-20", "2023-03-10"]


# Одинаковые даты
def test_same_dates(data: List[List[Dict[str, Any]]]) -> None:
    result = sort_by_date(data[1])
    assert [d["date"] for d in result] == ["2023-03-10", "2023-03-10", "2023-01-15"]
    assert result[0]["id"] == 1


# Разные форматы дат
def test_diff_formats(data: List[List[Dict[str, Any]]]) -> None:
    result = sort_by_date(data[2])
    assert len(result) == 3


# Некорректные данные
def test_invalid_data(data: List[List[Dict[str, Any]]]) -> None:
    with pytest.raises(KeyError):
        sort_by_date(data[3])


# Пустой список
def test_empty(data: List[List[Dict[str, Any]]]) -> None:
    assert sort_by_date(data[4]) == []


# Нет ключа date
def test_missing_key() -> None:
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1}, {"date": "2023-01-01"}])


@pytest.mark.parametrize(
    "test_data, reverse, expected",
    [
        (
            [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "2023-01-15"}, {"id": 3, "date": "2023-02-20"}],
            True,
            ["2023-03-10", "2023-02-20", "2023-01-15"],
        ),
        (
            [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "2023-01-15"}, {"id": 3, "date": "2023-02-20"}],
            False,
            ["2023-01-15", "2023-02-20", "2023-03-10"],
        ),
        (
            [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "2023-01-15"}, {"id": 3, "date": "2023-03-10"}],
            True,
            ["2023-03-10", "2023-03-10", "2023-01-15"],
        ),
        (
            [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "15.01.2023"}, {"id": 3, "date": "2023/02/20"}],
            True,
            ["2023/02/20", "2023-03-10", "15.01.2023"],
        ),
        (
            [{"id": 1, "date": "2023-03-10"}, {"id": 2, "date": "не дата"}, {"id": 3, "date": ""}],
            True,
            ["не дата", "2023-03-10", ""],
        ),
        ([], True, []),
    ],
)
# Один тест на всё
def test_sort_by_date_with_param(
    test_data: List[Dict[str, Any]], reverse: bool, expected: Union[List[str], List]
) -> None:
    if expected == KeyError:
        with pytest.raises(KeyError):
            sort_by_date(test_data, reverse=reverse)
    else:
        result = sort_by_date(test_data, reverse=reverse)
        assert [d["date"] for d in result] == expected
