from typing import List

def processing(data: List, state: str='EXECUTED') -> List:
    if not data:
        return []
    else:
        return [item for item in data if item.get('state') == state]


def sort_by_date(next_data: List, reverse: bool=True) -> List:
    if not next_data:
        return []
    else:
        sorted_data = sorted(next_data, key=lambda x: x['date'], reverse=reverse)
        return sorted_data