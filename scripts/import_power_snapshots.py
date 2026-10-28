from datetime import datetime
from database import get_connection

def import_power_snapshots(power_data):
    """
    Schrijft 5-minuten snapshots weg naar SQLite.

    Verwacht een AlphaESS power endpoint response:
    {
        "ts": [...],
        "solar": [...],
        "battery": [...],
        "grid": [...],
        "evCharge": [...],
        "soc": [...]
    }
    """

    conn = get_connection()
    cur = conn.cursor()

    timestamps = power_data["ts"]

    solar = power_data.get("solar", [])
    battery = power_data.get("battery", [])
    grid = power_data.get("grid", [])
    ev_charge = power_data.get("evCharge", [])
    soc = power_data.get("soc", [])

    inserted = 0

    for i, ts in enumerate(timestamps):

        snapshot_time = datetime.fromisoformat(
            ts.replace("Z", "+00:00")
        )

        solar_w = float(solar[i]) if i < len(solar) else 0
        battery_w = float(battery[i]) if i < len(battery) else 0
        grid_w = float(grid[i]) if i < len(grid) else 0
        ev_w = float(ev_charge[i]) if i < len(ev_charge) else 0
        soc_pct = float(soc[i]) if i < len(soc) else None

        cur.execute("""
            INSERT OR REPLACE INTO power_snapshots (
                timestamp,
                solar_power_w,
                battery_power_w,
                grid_power_w,
                ev_power_w,
                battery_soc
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            snapshot_time.isoformat(),
            solar_w,
            battery_w,
            grid_w,
            ev_w,
            soc_pct
        ))

        inserted += 1

    conn.commit()
    conn.close()

    print(
        f"✅ {inserted} power snapshots imported."
    )