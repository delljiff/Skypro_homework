import re
from typing import Dict, List


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


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Принимает список словарей с банковскими операциями и строку поиска.
    Возвращает список словарей, у которых в описании есть данная строка.
    Использует библиотеку re для работы с регулярными выражениями.
    """
    if not search:
        # При пустой строке возвращаем все НЕПУСТЫЕ транзакции
        return [t for t in data if t]

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for transaction in data:
        if not transaction:  # пропускаем пустые словари
            continue
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict], categories: str) -> List[Dict]:
    """
        Принимает список словарей с банковскими операциями и список категорий.
        Возвращает словарь, где ключ — категория, значение — количество операций в этой категории.
        Категория определяется по полю description.

        Args:
            data: список словарей с транзакциями
            categories: список категорий для подсчета

        Returns:
            словарь {категория: количество}
    """
    from collections import Counter

    if not data or not categories:
        return {category: 0 for category in categories}

    matched = []
    for transaction in data:
        if not transaction:
            continue
        desc = transaction.get('description', '')
        if desc in categories:
            matched.append(desc)

    counter = Counter(matched)

    return {category: counter.get(category, 0) for category in categories}
