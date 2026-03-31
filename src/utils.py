import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список транзакций или пустой список, если файла нет или он повреждён
    """
    logger.debug(f"Попытка загрузить файл: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return []

    if isinstance(data, list):
        logger.info(f"Успешно загружено {len(data)} транзакций")
        return data
    else:
        logger.error("Неверный формат данных: ожидался список")
        return []
