import sqlite3
import json

from pathlib import Path
from datetime import datetime

from cost_engine import (
    calculate_session_market_price
)


ARCHIVE_FILE = (
    Path("price_history") /
    "price_archive.json"
)


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

try:
    cur.execute(
        "ALTER TABLE sessions ADD COLUMN avg_price REAL"
    )
except:
    pass

try:
    cur.execute(
        "ALTER TABLE sessions ADD COLUMN market_cost REAL"
    )
except:
    pass


print("Prijsarchief laden...")

with open(
    ARCHIVE_FILE,
    encoding="utf-8"
) as f:

    archive = json.load(f)


price_lookup = {}

for key, value in archive.items():

    ts = datetime.fromisoformat(
        key
    )

    price_lookup[ts] = float(
        value
    )


cur.execute(
    """
    SELECT
        id,
        start_time,
        end_time,
        kwh
    FROM sessions
    """
)

rows = cur.fetchall()


updated = 0

for row in rows:

    start_time = datetime.fromisoformat(
        row["start_time"]
        .replace(" ", "T")
    )

    end_time = datetime.fromisoformat(
        row["end_time"]
        .replace(" ", "T")
    )

    avg_price, market_cost = (
        calculate_session_market_price(
            start_time,
            end_time,
            row["kwh"],
            price_lookup
        )
    )

    cur.execute(
        """
        UPDATE sessions
        SET
            avg_price = ?,
            market_cost = ?
        WHERE id = ?
        """,
        (
            avg_price,
            market_cost,
            row["id"]
        )
    )

    updated += 1


conn.commit()

print()

print(
    f"{updated} sessies berekend."
)

print(
    "Market costs bijgewerkt."
)

print()