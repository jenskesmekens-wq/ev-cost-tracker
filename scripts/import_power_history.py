import os
import yaml
import sqlite3

from datetime import datetime
from datetime import timedelta

from alphaess_client import AlphaESSClient


with open(
    "config.yaml",
    encoding="utf-8"
) as f:

    cfg = yaml.safe_load(f)


client = AlphaESSClient(
    cfg["alphaess"]["email"],
    os.getenv(
        "ALPHAESS_PASSWORD"
    )
)

client.login()

conn = sqlite3.connect(
    "data/charging_history.db"
)

cur = conn.cursor()

start_date = datetime(
    2026,
    10,
    22
)

end_date = datetime(
    2026,
    10,
    28
)

current = start_date

inserted = 0

while current <= end_date:

    day_start = (
        current.strftime(
            "%Y-%m-%d"
        )
        + "T00:00:00Z"
    )

    day_end = (
        current.strftime(
            "%Y-%m-%d"
        )
        + "T23:59:59Z"
    )

    print(
        f"Importing {current.date()}"
    )

    data = client.get_power_history(
        day_start,
        day_end,
        5
    )

    for i in range(
        len(data["ts"])
    ):

        cur.execute("""
        INSERT OR REPLACE
        INTO power_snapshots (

            timestamp,

            solar_w,
            battery_w,
            grid_w,

            ev_w,
            load_w,

            soc

        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            data["ts"][i],
            data["solar"][i],
            data["battery"][i],
            data["grid"][i],
            data["evCharge"][i],
            data["load"][i],
            data["soc"][i]
        ))

        inserted += 1

    conn.commit()

    current += timedelta(
        days=1
    )

print()
print(
    f"{inserted} snapshots geïmporteerd"
)
print()
