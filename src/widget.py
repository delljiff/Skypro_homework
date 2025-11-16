from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_acc_data: str) -> str:
    """
    Функция принимает на вход название и номер карты или счета
    и маскирует его цифровую часть, как в предыдущих функциях
    """
    parts = card_or_acc_data.split()
    number_part = parts[-1]
    if number_part.isdigit() and len(number_part) == 20:
        if parts[0].lower() == "счет":
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
    return f"{unformatted_date[8:10]}.{unformatted_date[5:7]}.{unformatted_date[0:4]}"
