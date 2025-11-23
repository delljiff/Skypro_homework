from typing import List


def processing(data: List, state: str = "EXECUTED") -> List:
    """
    Функция сортирует список словарей по заранее известному параметру state
    """
    if not data:
        return []
    else:
        return [item for item in data if item.get("state") == state]


def sort_by_date(next_data: List, reverse: bool = True) -> List:
    """
    Функция для сортировки список словарей по параметру date по убыванию
    """
    if not next_data:
        return []
    else:
        sorted_data = sorted(next_data, key=lambda x: x["date"], reverse=reverse)
        return sorted_data
