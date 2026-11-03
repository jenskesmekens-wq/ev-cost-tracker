from pathlib import Path
import sqlite3

from battery_daily_ratios import (
    get_daily_battery_ratios
)


ROOT = Path(__file__).resolve().parent.parent

DB_FILE = (
    ROOT /
    "data" /
    "charging_history.db"
)


conn = sqlite3.connect(
    str(DB_FILE)
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

cur.execute("""
SELECT

    MIN(start_time),
    MAX(start_time)

FROM sessions
""")

row = cur.fetchone()

start_date = row[0][:10]
end_date = row[1][:10]

ratios = get_daily_battery_ratios(
    start_date,
    end_date
)

cur.execute("""
SELECT

    s.id,
    s.start_time,

    s.market_cost,

    b.pv_direct_kwh,
    b.battery_kwh,
    b.grid_direct_kwh

FROM sessions s

JOIN session_energy_breakdown b
ON s.id = b.session_id
""")

rows = cur.fetchall()

for row in rows:

    day = row["start_time"][:10]

    pv_ratio, grid_ratio = (
        ratios.get(
            day,
            (0.0, 1.0)
        )
    )

    pv_direct = (
        row["pv_direct_kwh"] or 0
    )

    battery = (
        row["battery_kwh"] or 0
    )

    grid_direct = (
        row["grid_direct_kwh"] or 0
    )

    total_energy = (
        pv_direct +
        battery +
        grid_direct
    )

    if total_energy <= 0:
        continue

    battery_grid = (
        battery *
        grid_ratio
    )

    effective_grid = (
        grid_direct +
        battery_grid
    )

    ratio = (
        effective_grid /
        total_energy
    )

    market_cost = (
        row["market_cost"] or 0
    )

    actual_cost = (
        market_cost *
        ratio
    )

    savings = (
        market_cost -
        actual_cost
    )

    cur.execute("""
    UPDATE sessions
    SET
        actual_cost=?,
        savings=?
    WHERE id=?
    """,
    (
        round(
            actual_cost,
            2
        ),
        round(
            savings,
            2
        ),
        row["id"]
    ))

conn.commit()

print()
print(
    f"Actual costs recalculated "
    f"({start_date} → {end_date})"
)
print()