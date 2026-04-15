import csv
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Файл пуст: {file_path}")

    transactions = []

    with open(path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")

        for row in reader:
            cleaned_row = {}
            for key, value in row.items():
                cleaned_row[key] = value if value != "" else None

            if all(v is None for v in cleaned_row.values()):
                continue

            transactions.append(cleaned_row)

    return transactions


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        df = pd.read_excel(path)

        if df.empty:
            raise ValueError("Excel файл не содержит данных")

        df = df.replace("", None)

        transactions = df.to_dict(orient="records")

        transactions = [row for row in transactions if any(pd.notna(value) and value != "" for value in row.values())]

        if not transactions:
            raise ValueError("Excel файл не содержит данных после очистки")

        return transactions

    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel файла: {e}")
