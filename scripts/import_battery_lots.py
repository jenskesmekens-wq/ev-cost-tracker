# import_battery_lots.py

import json
import sqlite3
from datetime import datetime, timezone

DB = "charging_history.db"

def connect():
    return sqlite3.connect(DB)

def ensure_indexes(conn):
    conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_battery_lots_unique
    ON battery_lots(timestamp, source, energy_kwh)
    """)
    conn.commit()

def create_battery_lot(
    conn,
    ts,
    source,
    energy_kwh,
    unit_cost
):
    conn.execute("""
    INSERT OR IGNORE INTO battery_lots
    (
        timestamp,
        source,
        remaining_kwh,
        original_kwh,
        cost_per_kwh
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        ts,
        source,
        energy_kwh,
        energy_kwh,
        unit_cost
    ))

def import_json(
    json_path,
    grid_price_lookup
):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = connect()
    ensure_indexes(conn)

    ts = data["ts"]
    battery = data["battery"]
    solar = data["solar"]
    grid = data["grid"]

    for i in range(len(ts)):

        timestamp = ts[i]

        battery_power = float(battery[i])
        solar_power = float(solar[i])
        grid_power = float(grid[i])

        #
        # aannames:
        #
        # battery < 0  => laden
        # battery > 0  => ontladen
        #
        if battery_power >= 0:
            continue

        charge_power_w = abs(battery_power)

        #
        # 5 minuten interval
        #
        energy_kwh = charge_power_w / 1000 * (5 / 60)

        if energy_kwh < 0.01:
            continue

        #
        # bron bepalen
        #
        grid_import = max(grid_power, 0)

        if grid_import > 200:
            source = "GRID"
            unit_cost = grid_price_lookup(timestamp)

        else:
            source = "PV"
            unit_cost = 0.0

        create_battery_lot(
            conn,
            timestamp,
            source,
            round(energy_kwh, 4),
            unit_cost
        )

    conn.commit()
    conn.close()


def grid_price_lookup(timestamp):
    """
    Tijdelijke placeholder.

    Later koppelen aan
    prices.json / existing price engine.
    """

    dt = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    return 0.15


if __name__ == "__main__":
    import_json(
        "alpha_5min.json",
        grid_price_lookup
    )

    print("Battery lots imported.")