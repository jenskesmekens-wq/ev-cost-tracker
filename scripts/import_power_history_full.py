import os
import yaml
import sqlite3

from datetime import datetime
from datetime import timedelta

from alphaess_client import AlphaESSClient


CONFIG = "config.yaml"


def daterange(start, end):

    current = start

    while current <= end:

        yield current

        current += timedelta(days=1)


def load_config():

    with open(
        CONFIG,
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)


def get_sync_dates(conn):

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT
        MIN(start_time)
    FROM sessions
    """)

    row = cur.fetchone()

    if not row or not row[0]:

        raise RuntimeError(
            "Geen sessies gevonden in database."
        )

    start_date = datetime.fromisoformat(
        row[0].replace(" ", "T")
    )

    end_date = datetime.today()

    return (
        start_date,
        end_date
    )


def valid_power_response(data):

    if not data:
        return False

    if not isinstance(
        data,
        dict
    ):
        return False

    if "ts" not in data:
        return False

    if not data["ts"]:
        return False

    return True


def main():

    cfg = load_config()

    client = AlphaESSClient(
        cfg["alphaess"]["email"],
        os.getenv(
            "ALPHAESS_PASSWORD",
            ""
        )
    )

    client.login()

    conn = sqlite3.connect(
        cfg["database"]["path"]
    )

    cur = conn.cursor()

    start_date, end_date = (
        get_sync_dates(conn)
    )

    print()
    print(
        f"Synchroniseren van "
        f"{start_date.date()} "
        f"tot "
        f"{end_date.date()}"
    )
    print()

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
            f"Importing "
            f"{day.strftime('%Y-%m-%d')}"
        )

        try:

            data = client.get_power_history(
                begin,
                end,
                5
            )

        except Exception as ex:

            print(
                f"FAILED: "
                f"{day.strftime('%Y-%m-%d')}"
            )

            print(ex)

            continue

        if not valid_power_response(
            data
        ):

            print(
                f"Geen geldige power history "
                f"voor "
                f"{day.strftime('%Y-%m-%d')}"
            )

            continue

        count = len(
            data["ts"]
        )

        for i in range(count):

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

                data.get(
                    "solar",
                    []
                )[i],

                data.get(
                    "battery",
                    []
                )[i],

                data.get(
                    "grid",
                    []
                )[i],

                data.get(
                    "evCharge",
                    []
                )[i],

                data.get(
                    "load",
                    []
                )[i],

                data.get(
                    "soc",
                    []
                )[i]
            ))

            total_inserted += 1

        conn.commit()

    conn.close()

    print()
    print(
        f"TOTAL SNAPSHOTS IMPORTED: "
        f"{total_inserted}"
    )
    print()


if __name__ == "__main__":

    main()