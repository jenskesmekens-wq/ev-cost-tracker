import json
import requests

from pathlib import Path
from datetime import datetime, timedelta


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

ARCHIVE_FILE = (
    PRICE_HISTORY /
    "price_archive.json"
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

    today = datetime.now().date()

    if day_name == "today":

        day_string = (
            today.isoformat()
        )

    elif day_name == "tomorrow":

        day_string = (
            (
                today +
                timedelta(days=1)
            ).isoformat()
        )

    else:

        return

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
        f"Opgeslagen: "
        f"{file_path}"
    )


def update_archive():

    archive = {}

    if ARCHIVE_FILE.exists():

        with open(
            ARCHIVE_FILE,
            encoding="utf-8"
        ) as f:

            archive = json.load(f)

    for file in sorted(
        PRICE_HISTORY.glob(
            "*.json"
        )
    ):

        if (
            file.name
            ==
            "price_archive.json"
        ):
            continue

        with open(
            file,
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        for item in data.get(
            "data",
            []
        ):

            utc_dt = (
                datetime
                .fromisoformat(
                    item["timestamp"]
                    .replace(
                        "Z",
                        "+00:00"
                    )
                )
            )

            local_dt = (
                utc_dt +
                timedelta(hours=1)
            )

            key = (
                local_dt.strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )
            )

            archive[key] = float(
                item["price_eur_kwh"]
            )

    with open(
        ARCHIVE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            archive,
            f,
            indent=2,
            ensure_ascii=False,
            sort_keys=True
        )

    print()
    print(
        f"{len(archive)} "
        f"kwartierprijzen "
        f"in archief"
    )
    print()


def main():

    print()
    print(
        "Prijzen ophalen..."
    )
    print()

    response = requests.get(
        PRICE_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    save_day(
        "today",
        data.get("today")
    )

    save_day(
        "tomorrow",
        data.get("tomorrow")
    )

    update_archive()

    print()
    print(
        "Price history bijgewerkt"
    )
    print()


if __name__ == "__main__":

    main()