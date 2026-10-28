import json
from pathlib import Path


def load_day_prices(day_string):

    file_path = (
        Path("price_history")
        / f"{day_string}.json"
    )

    if not file_path.exists():
        return None

    with open(
        file_path,
        encoding="utf-8"
    ) as f:

        return json.load(f)