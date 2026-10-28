from datetime import datetime
import sqlite3

DB_PATH = "charging_history.db"

SITE_BATTERY_KWH = 10.0  # aanpassen indien nodig
INTERVAL_HOURS = 5 / 60  # 5 minuten

def create_battery_lot(cur, ts, source, energy_kwh, cost_per_kwh):
    if energy_kwh <= 0:
        return

    cur.execute("""
        INSERT INTO battery_lots
        (
            timestamp,
            source,
            energy_kwh,
            remaining_kwh,
            cost_per_kwh
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        ts,
        source,
        energy_kwh,
        energy_kwh,
        cost_per_kwh
    ))

def get_hour_price(ts):
    """
    Gebruik jouw bestaande prijsfunctie.
    Tijdelijk 0 teruggeven tot koppeling gemaakt is.
    """

    return 0.0

def process_power_json(power_data):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    ts_list = power_data["ts"]
    battery_list = power_data["battery"]
    solar_list = power_data["solar"]
    grid_list = power_data["grid"]

    for i in range(len(ts_list)):

        ts = ts_list[i]

        battery_power = battery_list[i]
        solar_power = solar_list[i]
        grid_power = grid_list[i]

        #
        # AlphaESS:
        # battery < 0 = laden
        # battery > 0 = ontladen
        #

        if battery_power >= 0:
            continue

        charge_power_w = abs(battery_power)

        energy_kwh = (
            charge_power_w
            * INTERVAL_HOURS
            / 1000
        )

        pv_available = max(solar_power, 0)

        grid_import = max(grid_power, 0)

        total_supply = pv_available + grid_import

        if total_supply <= 0:
            continue

        pv_ratio = pv_available / total_supply
        grid_ratio = grid_import / total_supply

        pv_energy = energy_kwh * pv_ratio
        grid_energy = energy_kwh * grid_ratio

        if pv_energy > 0:

            create_battery_lot(
                cur,
                ts,
                "PV",
                pv_energy,
                0.0
            )

        if grid_energy > 0:

            create_battery_lot(
                cur,
                ts,
                "GRID",
                grid_energy,
                get_hour_price(ts)
            )

    conn.commit()
    conn.close()

    print("Battery lots generated.")