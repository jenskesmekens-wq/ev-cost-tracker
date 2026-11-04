import json

from pathlib import Path
from datetime import datetime, timedelta


PRICE_HISTORY = Path(
    "price_history"
)

ARCHIVE_FILE = (
    PRICE_HISTORY /
    "price_archive.json"
)


archive = {}


for file in sorted(
    PRICE_HISTORY.glob("*.json")
):

    if file.name == "price_archive.json":
        continue

    print(
        f"Verwerken: {file.name}"
    )

    with open(
        file,
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    for item in data.get(
        "data",
        []
    ):

        utc_dt = datetime.fromisoformat(
            item["timestamp"]
            .replace("Z", "+00:00")
        )

        local_dt = (
            utc_dt +
            timedelta(hours=1)
        )

        key = local_dt.strftime(
            "%Y-%m-%dT%H:%M:%S"
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
    f"{len(archive)} kwartierprijzen opgeslagen"
)
print(
    f"Bestand: {ARCHIVE_FILE}"
)
print()