import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_DIR / "masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция для маскировки номера карты."""
    logger.debug(f"Начало маскирования карты: {card_number}")
    if card_number.isdigit() and len(card_number) == 16:
        mask = "*" * len(card_number[6:-4])
        masked_card_number = card_number[0:6] + mask + card_number[-4:]
        result_1 = ""
        for i in range(0, len(masked_card_number), 4):
            result_1 += masked_card_number[i : i + 4] + " "
        result = result_1.strip()
        logger.info(f"Успешно замаскирован номер карты: {result}")
        return result
    else:
        logger.error(f"Ошибка: неверный номер карты {card_number}")
        return "Вы неверно ввели номер карты"


def get_mask_account(account_number: str) -> str:
    """Функция для маскировки номера счета."""
    logger.debug(f"Начало маскирования счета: {account_number}")
    if account_number.isdigit() and len(account_number) == 20:
        secret = "**"
        last_digits = account_number[-4:]
        result_2 = secret + last_digits
        logger.info(f"Успешно замаскирован номер счета: {result_2}")
        return result_2
    else:
        logger.error(f"Ошибка: неверный номер счета {account_number}")
        return "Вы неверно ввели номер счета"
