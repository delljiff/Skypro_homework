from typing import List, Dict


def filter_by_state(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция сортирует список словарей по заранее известному параметру state
    """
    if not data:
        return []
    else:
        return [item for item in data if item.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Функция для сортировки список словарей по параметру date по убыванию
    """
    if not transactions:
        return []
    else:
        sorted_data = sorted(transactions, key=lambda x: x["date"], reverse=reverse)
        return sorted_data
