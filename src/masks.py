def get_mask_card_number(card_number: str) -> str:
    """Функция для маскировки номера карты."""
    if card_number.isdigit() and len(card_number) == 16:
        mask = "*" * len(card_number[6:-4])
        masked_card_number = card_number[0:6] + mask + card_number[-4:]
        result_1 = ""
        for i in range(0, len(masked_card_number), 4):
            result_1 += masked_card_number[i : i + 4] + " "
        return result_1
    else:
        return "Вы неверно ввели номер карты"


def get_mask_account(account_number: str) -> str:
    """Функция для маскировки номера счета."""
    if account_number.isdigit() and len(account_number) == 20:
        secret = "**"
        last_digits = account_number[-4:]
        result_2 = secret + last_digits
        return result_2
    else:
        return "Вы неверно ввели номер счета"
