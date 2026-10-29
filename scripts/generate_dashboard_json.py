import sqlite3
import json

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

sessions = []

total_loaded = 0
total_market = 0
total_actual = 0
total_savings = 0

pv_direct_total = 0
battery_pv_total = 0
battery_grid_total = 0
grid_direct_total = 0

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
        battery * pv_ratio
    )

    battery_grid = (
        battery * grid_ratio
    )

    total_loaded += (
        row["kwh"] or 0
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

    pv_direct_total += pv_direct
    battery_pv_total += battery_pv
    battery_grid_total += battery_grid
    grid_direct_total += grid_direct

    sessions.append({

        "date":
        row["start_time"],

        "kwh":
        round(
            row["kwh"] or 0,
            2
        ),

        "pv_direct":
        round(
            pv_direct,
            2
        ),

        "battery_pv":
        round(
            battery_pv,
            2
        ),

        "battery_grid":
        round(
            battery_grid,
            2
        ),

        "grid_direct":
        round(
            grid_direct,
            2
        ),

        "market_cost":
        round(
            row["market_cost"] or 0,
            2
        ),

        "actual_cost":
        round(
            row["actual_cost"] or 0,
            2
        ),

        "savings":
        round(
            row["savings"] or 0,
            2
        )

    })

dashboard = {

    "summary": {

        "total_loaded":
        round(
            total_loaded,
            2
        ),

        "market_cost":
        round(
            total_market,
            2
        ),

        "actual_cost":
        round(
            total_actual,
            2
        ),

        "total_savings":
        round(
            total_savings,
            2
        ),

        "avg_market_price":
        round(
            total_market /
            total_loaded,
            4
        ) if total_loaded else 0,

        "avg_actual_price":
        round(
            total_actual /
            total_loaded,
            4
        ) if total_loaded else 0
    },

    "energy_split": {

        "pv_direct":
        round(
            pv_direct_total,
            2
        ),

        "battery_pv":
        round(
            battery_pv_total,
            2
        ),

        "battery_grid":
        round(
            battery_grid_total,
            2
        ),

        "grid_direct":
        round(
            grid_direct_total,
            2
        )
    },

    "latest_session":
    sessions[0] if sessions else {},

    "sessions":
    sessions
}

with open(
    "docs/dashboard.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        dashboard,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(
    "docs/dashboard.json gegenereerd"
)
print()