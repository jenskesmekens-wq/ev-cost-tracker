import json
import requests

from pathlib import Path
from datetime import datetime


PRICE_URL = (
    "https://jenskesmekens-wq.github.io/"
    "Energieprijs-v4/prices.json"
)

PRICE_HISTORY = Path(
    "price_history"
)

PRICE_HISTORY.mkdir(
    exist_ok=True
)


def save_day(day_name, day_data):

    if not day_data:
        return

    items = day_data.get(
        "data",
        []
    )

    if not items:
        return

    day_string = (
        datetime.fromisoformat(
            items[0]["timestamp"]
            .replace("Z", "+00:00")
        )
        .date()
        .isoformat()
    )

    file_path = (
        PRICE_HISTORY /
        f"{day_string}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            day_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Opgeslagen: {file_path}"
    )


def main():

    print()
    print("Prijzen ophalen...")
    print()

    data = requests.get(
        PRICE_URL,
        timeout=30
    ).json()

    save_day(
        "today",
        data.get("today")
    )

    save_day(
        "tomorrow",
        data.get("tomorrow")
    )

    print()
    print(
        "Price history bijgewerkt"
    )
    print()


if __name__ == "__main__":

    main()