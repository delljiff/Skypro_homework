from typing import Any, Dict, Generator, Iterator


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """
    Функция, которая фильтрует список странзакций (словари) по определенному курсу валют
    """
    for transaction in transactions:
        if transaction["currency"] == currency:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор, который из списка транзакций возвращает последовательность описаний каждой операции
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор для создания номеров карт исходя из диапазона чисел
    """
    for num in range(start, stop + 1):
        formatted_number = "{:04d} {:04d} {:04d} {:04d}".format(
            num // 10**12, (num // 10**8) % 10**4, (num // 10**4) % 10**4, num % 10**4
        )
        yield formatted_number
