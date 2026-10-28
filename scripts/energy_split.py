import sqlite3


def calculate_energy_flows(conn):

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM power_snapshots
    ORDER BY timestamp
    """)

    rows = cur.fetchall()

    totals = {
        "pv_kwh": 0.0,
        "battery_kwh": 0.0,
        "grid_kwh": 0.0,
        "ev_kwh": 0.0
    }

    for row in rows:

        solar_w = row["solar_w"] or 0
        battery_w = row["battery_w"] or 0
        grid_w = row["grid_w"] or 0
        ev_w = row["ev_w"] or 0

        hours = 5 / 60

        ev_kwh = (
            ev_w *
            hours
        ) / 1000

        #
        # Alleen rekening houden met
        # tijdstippen waarop effectief geladen werd
        #
        if ev_kwh <= 0:
            continue

        pv_kwh = (
            max(0, solar_w)
            * hours
        ) / 1000

        battery_kwh = (
            max(0, abs(battery_w))
            * hours
        ) / 1000

        grid_kwh = (
            max(0, grid_w)
            * hours
        ) / 1000

        totals["ev_kwh"] += ev_kwh
        totals["pv_kwh"] += pv_kwh
        totals["battery_kwh"] += battery_kwh
        totals["grid_kwh"] += grid_kwh

    return totals