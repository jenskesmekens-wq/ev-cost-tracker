import sqlite3


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

cur.execute("""
SELECT

    s.start_time,

    s.kwh,

    s.market_cost,
    s.actual_cost,
    s.savings,

    b.pv_direct_kwh,
    b.battery_kwh,
    b.grid_direct_kwh

FROM sessions s

LEFT JOIN session_energy_breakdown b
ON s.id = b.session_id

ORDER BY s.start_time DESC
""")

rows = cur.fetchall()

print()
print("=" * 90)
print("EV COST TRACKER V2")
print("=" * 90)
print()

total_market = 0
total_actual = 0
total_savings = 0
total_kwh = 0

for row in rows:

    total_market += row["market_cost"] or 0
    total_actual += row["actual_cost"] or 0
    total_savings += row["savings"] or 0
    total_kwh += row["kwh"] or 0

    pv = row["pv_direct_kwh"] or 0
    battery = row["battery_kwh"] or 0
    grid = row["grid_direct_kwh"] or 0

    energy_total = pv + battery + grid

    pv_pct = 0
    battery_pct = 0
    grid_pct = 0

    if energy_total > 0:

        pv_pct = (
            pv / energy_total
        ) * 100

        battery_pct = (
            battery / energy_total
        ) * 100

        grid_pct = (
            grid / energy_total
        ) * 100

    print(
        f"Datum      : {row['start_time']}"
    )

    print(
        f"kWh        : {row['kwh']}"
    )

    print()

    print(
        f"PV         : "
        f"{round(pv,2)} kWh "
        f"({round(pv_pct,1)}%)"
    )

    print(
        f"Batterij   : "
        f"{round(battery,2)} kWh "
        f"({round(battery_pct,1)}%)"
    )

    print(
        f"Net        : "
        f"{round(grid,2)} kWh "
        f"({round(grid_pct,1)}%)"
    )

    print()

    print(
        f"Marktkost  : "
        f"€{round(row['market_cost'] or 0,2)}"
    )

    print(
        f"Werkelijk  : "
        f"€{round(row['actual_cost'] or 0,2)}"
    )

    print(
        f"Besparing  : "
        f"€{round(row['savings'] or 0,2)}"
    )

    print("-" * 90)

print()
print("=" * 90)
print("TOTAAL")
print("=" * 90)

print(
    f"Totaal kWh       : "
    f"{round(total_kwh,2)}"
)

print(
    f"Marktkost        : "
    f"€{round(total_market,2)}"
)

print(
    f"Werkelijke kost  : "
    f"€{round(total_actual,2)}"
)

print(
    f"Besparing        : "
    f"€{round(total_savings,2)}"
)

if total_kwh > 0:

    print(
        f"Gem €/kWh markt  : "
        f"€{round(total_market / total_kwh,4)}"
    )

    print(
        f"Gem €/kWh echt   : "
        f"€{round(total_actual / total_kwh,4)}"
    )

print()