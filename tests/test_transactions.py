from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.transactions import read_csv_transactions, read_excel_transactions

# ========== ТЕСТЫ ДЛЯ CSV ==========


def test_read_csv_success():
    """Тест: успешное чтение CSV файла"""
    mock_csv_content = "id;state;amount\n" "1;EXECUTED;100\n" "2;PENDING;200\n"

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.stat") as mock_stat:
                mock_stat.return_value.st_size = len(mock_csv_content)
                result = read_csv_transactions("fake.csv")

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[0]["state"] == "EXECUTED"
    assert result[0]["amount"] == "100"
    assert result[1]["id"] == "2"


def test_read_csv_file_not_found():
    """Тест: CSV файл не существует"""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Файл не найден"):
            read_csv_transactions("nonexistent.csv")


def test_read_csv_empty_file():
    """Тест: CSV файл пустой"""
    with patch("builtins.open", mock_open(read_data="")):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.stat") as mock_stat:
                mock_stat.return_value.st_size = 0
                with pytest.raises(ValueError, match="Файл пуст"):
                    read_csv_transactions("empty.csv")


def test_read_csv_skips_empty_rows():
    """Тест: CSV с пустыми строками пропускает их"""
    mock_csv_content = "id;state;amount\n" "1;EXECUTED;100\n" ";;\n" "2;PENDING;200\n"

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.stat") as mock_stat:
                mock_stat.return_value.st_size = len(mock_csv_content)
                result = read_csv_transactions("fake.csv")

    # Пустая строка должна быть пропущена
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"


# ========== ТЕСТЫ ДЛЯ EXCEL ==========


def test_read_excel_success():
    """Тест: успешное чтение Excel файла"""
    # Создаём фейковый DataFrame
    mock_df = pd.DataFrame({"id": [1, 2], "state": ["EXECUTED", "PENDING"], "amount": [100, 200]})

    with patch("pandas.read_excel", return_value=mock_df):
        with patch("pathlib.Path.exists", return_value=True):
            result = read_excel_transactions("fake.xlsx")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["state"] == "EXECUTED"
    assert result[0]["amount"] == 100


def test_read_excel_file_not_found():
    """Тест: Excel файл не существует"""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Файл не найден"):
            read_excel_transactions("nonexistent.xlsx")


def test_read_excel_empty_file():
    """Тест: Excel файл пустой"""
    mock_df = pd.DataFrame()  # Пустой DataFrame

    with patch("pandas.read_excel", return_value=mock_df):
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(ValueError, match="Excel файл не содержит данных"):
                read_excel_transactions("empty.xlsx")


def test_read_excel_removes_empty_rows():
    """Тест: Excel с пустыми строками удаляет их"""
    # Создаём DataFrame с пустой строкой
    mock_df = pd.DataFrame({"id": [1, None, 2], "state": ["EXECUTED", None, "PENDING"], "amount": [100, None, 200]})

    with patch("pandas.read_excel", return_value=mock_df):
        with patch("pathlib.Path.exists", return_value=True):
            result = read_excel_transactions("fake.xlsx")

    # Пустая строка (где всё None) должна быть удалена
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_read_excel_corrupted():
    """Тест: повреждённый Excel файл"""
    with patch("pandas.read_excel", side_effect=Exception("File corrupted")):
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(ValueError, match="Ошибка при чтении Excel файла"):
                read_excel_transactions("corrupted.xlsx")
