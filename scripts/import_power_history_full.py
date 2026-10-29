import os
import yaml
import sqlite3

from datetime import datetime
from datetime import timedelta

from alphaess_client import AlphaESSClient


START_DATE = "2026-10-15"
END_DATE = "2026-10-28"


def daterange(start, end):

    current = start

    while current <= end:

        yield current

        current += timedelta(days=1)


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

start_date = datetime.strptime(
    START_DATE,
    "%Y-%m-%d"
)

end_date = datetime.strptime(
    END_DATE,
    "%Y-%m-%d"
)

total_inserted = 0

for day in daterange(
    start_date,
    end_date
):

    begin = (
        day.strftime(
            "%Y-%m-%d"
        )
        + "T00:00:00Z"
    )

    end = (
        day.strftime(
            "%Y-%m-%d"
        )
        + "T23:59:59Z"
    )

    print(
        f"Importing {day.strftime('%Y-%m-%d')}"
    )

    try:

        data = client.get_power_history(
            begin,
            end,
            5
        )

    except Exception as ex:

        print(
            f"FAILED: {day.strftime('%Y-%m-%d')}"
        )

        print(ex)

        continue

    count = len(
        data["ts"]
    )

    for i in range(count):

        cur.execute("""
        INSERT OR REPLACE INTO power_snapshots (

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

        total_inserted += 1

    conn.commit()

print()
print(
    f"TOTAL SNAPSHOTS IMPORTED: {total_inserted}"
)
print()