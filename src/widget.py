from masks import get_mask_card_number
from masks import get_mask_account


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
            return f'Счет {masked}'
    elif number_part.isdigit() and len(number_part) == 16:
        card_num = number_part
        card_title = " ".join(parts[:-1])
        masked_num = get_mask_card_number(card_num)
        return f'{card_title} {masked_num}'
    else:
        return 'Неверно введены данные'
