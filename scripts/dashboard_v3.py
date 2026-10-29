import sqlite3

from battery_daily_ratios import (
    get_daily_battery_ratios
)


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

ratios = get_daily_battery_ratios(
    "2026-10-22",
    "2026-10-28"
)

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
print("=" * 100)
print("EV COST TRACKER V3")
print("=" * 100)
print()

total_market = 0
total_actual = 0
total_savings = 0
total_kwh = 0

total_pv_direct = 0
total_battery_pv = 0
total_battery_grid = 0
total_grid_direct = 0

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

    battery_pv = (
        battery *
        pv_ratio
    )

    battery_grid = (
        battery *
        grid_ratio
    )

    total_market += (
        row["market_cost"] or 0
    )

    total_actual += (
        row["actual_cost"] or 0
    )

    total_savings += (
        row["savings"] or 0
    )

    total_kwh += (
        row["kwh"] or 0
    )

    total_pv_direct += pv_direct
    total_battery_pv += battery_pv
    total_battery_grid += battery_grid
    total_grid_direct += grid_direct

    print(
        f"Datum            : {row['start_time']}"
    )

    print(
        f"kWh geladen      : {row['kwh']}"
    )

    print()

    print(
        f"Direct PV        : "
        f"{round(pv_direct,2)} kWh"
    )

    print(
        f"Battery PV       : "
        f"{round(battery_pv,2)} kWh"
    )

    print(
        f"Battery GRID     : "
        f"{round(battery_grid,2)} kWh"
    )

    print(
        f"Direct GRID      : "
        f"{round(grid_direct,2)} kWh"
    )

    print()

    print(
        f"Marktkost        : "
        f"€{round(row['market_cost'] or 0,2)}"
    )

    print(
        f"Werkelijke kost  : "
        f"€{round(row['actual_cost'] or 0,2)}"
    )

    print(
        f"Besparing        : "
        f"€{round(row['savings'] or 0,2)}"
    )

    print("-" * 100)

print()
print("=" * 100)
print("TOTAAL")
print("=" * 100)

print(
    f"Totaal geladen       : "
    f"{round(total_kwh,2)} kWh"
)

print()

print(
    f"Direct PV            : "
    f"{round(total_pv_direct,2)} kWh"
)

print(
    f"Battery PV           : "
    f"{round(total_battery_pv,2)} kWh"
)

print(
    f"Battery GRID         : "
    f"{round(total_battery_grid,2)} kWh"
)

print(
    f"Direct GRID          : "
    f"{round(total_grid_direct,2)} kWh"
)

print()

print(
    f"Marktkost            : "
    f"€{round(total_market,2)}"
)

print(
    f"Werkelijke kost      : "
    f"€{round(total_actual,2)}"
)

print(
    f"Totale besparing     : "
    f"€{round(total_savings,2)}"
)

if total_kwh > 0:

    print()

    print(
        f"Gem €/kWh markt      : "
        f"€{round(total_market / total_kwh,4)}"
    )

    print(
        f"Gem €/kWh werkelijk  : "
        f"€{round(total_actual / total_kwh,4)}"
    )

print()