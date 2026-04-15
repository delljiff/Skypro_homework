from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_acc_data: str) -> str:
    """
    Функция принимает на вход название и номер карты или счета
    и маскирует его цифровую часть, как в предыдущих функциях
    """
    if not card_or_acc_data:
        return "Неверно введены данные"

    parts = card_or_acc_data.split()

    if len(parts) < 2:
        return "Неверно введены данные"

    number_part = parts[-1]
    if number_part.isdigit() and len(number_part) == 20:
        number_part = parts[-1]
        masked = get_mask_account(number_part)
        return f"Счет {masked}"
    elif number_part.isdigit() and len(number_part) == 16:
        card_num = number_part
        card_title = " ".join(parts[:-1])
        masked_num = get_mask_card_number(card_num)
        return f"{card_title} {masked_num}"
    else:
        return "Неверно введены данные"


def get_date(unformatted_date: str) -> str:
    """Функция преобразует поступаемую на вход дату в формат ДД.ММ.ГГГГ"""
    if not isinstance(unformatted_date, str) or len(unformatted_date) < 10:
        return "Неверный формат даты"

        # Извлекаем части даты
    year = unformatted_date[0:4]
    month = unformatted_date[5:7]
    day = unformatted_date[8:10]

    # Проверяем, что извлекли именно цифры
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return "Неверный формат даты"

    return f"{day}.{month}.{year}"
