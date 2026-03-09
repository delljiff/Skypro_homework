def filter_by_currency(transactions, currency):
    for transaction in transactions:
        if transaction["currency"] == currency:
            yield transaction


def transaction_descriptions(transactions):
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start, stop):
    for num in range(start, stop+1):
        formatted_number = "{:04d} {:04d} {:04d} {:04d}".format(
    num // 10**12, (num // 10**8) % 10**4, (num // 10**4) % 10**4, num % 10**4
)
        yield formatted_number





