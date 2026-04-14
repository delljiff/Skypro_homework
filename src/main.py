import os
import sys

from file_reader import read_csv, read_json, read_xlsx


def mask_account(number: str) -> str:
    """Маскирует номер счета или карты."""
    if not number:
        return ""

    if "Счет" in number:
        # Для счета: Счет **1234
        digits = number.replace("Счет ", "")
        if digits.isdigit():
            return f"Счет **{digits[-4:]}"
        return number

    # Для карты: Visa Platinum 1234 12** **** 5678
    parts = number.split()
    if len(parts) >= 2:
        # Последняя часть - номер карты
        card_number = parts[-1]
        if card_number.isdigit() and len(card_number) == 16:
            # Остальные части - название карты (Visa, MasterCard и т.д.)
            card_type = " ".join(parts[:-1])
            return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return number


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_transactions(choice: str) -> list:
    """Загружает транзакции из выбранного файла."""
    if choice == "1":
        filepath = "data/operations.json"
        return read_json(filepath)
    elif choice == "2":
        filepath = "data/transactions.csv"
        return read_csv(filepath)
    else:
        filepath = "data/transactions_excel.xlsx"
        return read_xlsx(filepath)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Ваш выбор (1/2/3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")

    transactions = load_transactions(choice)

    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
    else:
        print("\nДля обработки выбран XLSX-файл.")

    print(f"Загружено транзакций: {len(transactions)}")

    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    selected_status = get_status_from_user()
    from src.processing import filter_by_state

    filtered_by_status = filter_by_state(transactions, selected_status)

    print(f"После фильтрации по статусу осталось транзакций: {len(filtered_by_status)}")

    if not filtered_by_status:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    need_sort, reverse = ask_sort_by_date()
    if need_sort:
        from src.processing import sort_by_date

        filtered_by_status = sort_by_date(filtered_by_status, reverse=reverse)
        print("Транзакции отсортированы по дате")

    ruble_only = ask_ruble_only()
    if ruble_only:
        filtered_by_status = filter_by_ruble(filtered_by_status)
        print("Оставлены только рублевые транзакции")

    search_string = ask_search_by_description()
    if search_string:
        from src.processing import process_bank_search

        filtered_by_status = process_bank_search(filtered_by_status, search_string)
        print(f"Отфильтровано по описанию. Осталось транзакций: {len(filtered_by_status)}")

    print(f"\nВсего банковских операций в выборке: {len(filtered_by_status)}")

    if not filtered_by_status:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    for t in filtered_by_status:
        # Форматируем дату из "2019-08-26T10:50:58.294041" в "26.08.2019"
        date_str = t.get("date", "")[:10]
        if date_str:
            date_formatted = f"{date_str[8:10]}.{date_str[5:7]}.{date_str[:4]}"
        else:
            date_formatted = "Дата неизвестна"

        print(f"\n{date_formatted} {t.get('description', '')}")

        from_info = t.get("from", "")
        to_info = t.get("to", "")
        if from_info and to_info:
            print(f"{mask_account(from_info)} -> {mask_account(to_info)}")
        elif to_info:
            print(f"{mask_account(to_info)}")

        amount = t.get("amount", 0)
        currency = t.get("currency", "")
        print(f"Сумма: {amount} {currency}")

    print(f"\nВсего банковских операций в выборке: {len(filtered_by_status)}")


def get_status_from_user() -> str:
    """
    Запрашивает у пользователя статус операции.
    Повторяет запрос, пока не введен корректный статус.
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def ask_sort_by_date() -> tuple:
    """
    Спрашивает у пользователя, нужно ли сортировать по дате.
    Если да — спрашивает порядок (возрастание/убывание).
    Возвращает (нужно_ли_сортировать, направление_сортировки)
    """
    while True:
        answer = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()
        if answer in ["да", "нет"]:
            break
        print("Пожалуйста, ответьте 'Да' или 'Нет'")

    if answer == "нет":
        return False, None

    while True:
        order = input("Отсортировать по возрастанию или по убыванию?: ").strip().lower()
        if order in ["по возрастанию", "по убыванию"]:
            break
        print("Пожалуйста, ответьте 'по возрастанию' или 'по убыванию'")

    reverse = order == "по убыванию"
    return True, reverse


def ask_ruble_only() -> bool:
    """
    Спрашивает у пользователя, нужно ли оставить только рублевые транзакции.
    Возвращает True, если нужно фильтровать по рублям, иначе False.
    """
    while True:
        answer = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if answer in ["да", "нет"]:
            return answer == "да"
        print("Пожалуйста, ответьте 'Да' или 'Нет'")


def ask_search_by_description() -> str or None:
    """
    Спрашивает у пользователя, нужно ли фильтровать по описанию.
    Если да — запрашивает строку поиска и возвращает её.
    Если нет — возвращает None.
    """
    while True:
        answer = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        if answer in ["да", "нет"]:
            break
        print("Пожалуйста, ответьте 'Да' или 'Нет'")

    if answer == "нет":
        return None

    search_string = input("Введите слово или фразу для поиска: ").strip()
    return search_string if search_string else None


def filter_by_ruble(transactions: list) -> list:
    """Оставляет только транзакции с валютой RUB."""
    return [t for t in transactions if t.get("currency") == "RUB"]


if __name__ == "__main__":
    main()
