import sqlite3

from battery_ledger import (
    create_battery_lot
)


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

cur.execute("""
SELECT *
FROM power_snapshots
ORDER BY timestamp
""")

rows = cur.fetchall()

created = 0

for row in rows:

    timestamp = row["timestamp"]

    battery_w = row["battery_w"] or 0

    if battery_w >= 0:
        continue

    hours = 5 / 60

    battery_kwh = (
        abs(battery_w)
        * hours
    ) / 1000

    create_battery_lot(
        conn,
        timestamp,
        "UNKNOWN",
        battery_kwh,
        0
    )

    created += 1


print()

print(
    f"{created} battery lots aangemaakt"
)

print()