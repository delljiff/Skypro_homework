import json
import os


def load_transactions(file_path):
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

    if isinstance(data, list):
        return data
    else:
        return []