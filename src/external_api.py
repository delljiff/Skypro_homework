from typing import Any, Dict, Optional

import requests


def convert_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Принимает транзакцию и возвращает сумму в рублях (float).
    Если сумма уже в рублях — возвращает её.
    Если в USD или EUR — конвертирует через API.
    """
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return amount

    date_str = transaction["date"][:10]
    API_KEY = "VjFTNn5BJHX0nTryJEp8RqdKZ84KGN0K"

    url = f"https://api.apilayer.com/exchangerates_data/{date_str}?base={currency_code}&symbols=RUB"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        rate = data["rates"]["RUB"]
        return round(amount * rate, 2)
    else:
        return None
