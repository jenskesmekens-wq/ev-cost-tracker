from database import get_connection

BATTERY_THRESHOLD_W = 100

def build_battery_ledger():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            timestamp,
            battery_power_w
        FROM power_snapshots
        ORDER BY timestamp
    """)

    rows = cur.fetchall()

    created = 0

    for i in range(len(rows) - 1):

        ts = rows[i]["timestamp"]

        battery_w = rows[i]["battery_power_w"]

        #
        # Negatief = laden batterij
        #
        if battery_w >= -BATTERY_THRESHOLD_W:
            continue

        charge_power_w = abs(battery_w)

        #
        # 5 minuten interval
        #
        energy_kwh = (
            charge_power_w
            * (5 / 60)
        ) / 1000

        cur.execute("""
            INSERT INTO battery_lots (
                created_at,
                source,
                energy_kwh,
                remaining_kwh,
                cost_per_kwh
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ts,
            "UNKNOWN",
            energy_kwh,
            energy_kwh,
            0
        ))

        created += 1

    conn.commit()
    conn.close()

    print(
        f"✅ {created} battery lots created."
    )

if __name__ == "__main__":
    build_battery_ledger()