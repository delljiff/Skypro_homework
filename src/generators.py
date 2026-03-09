def filter_by_currency(transactions, currency):
    for transaction in transactions:
        if transaction["currency"] == currency:
            yield transaction


def transaction_descriptions(transactions):
    for transaction in transactions:
        yield transaction["description"]


