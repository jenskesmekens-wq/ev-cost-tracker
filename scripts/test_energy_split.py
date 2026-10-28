import sqlite3

from energy_split import (
    calculate_energy_flows
)

conn = sqlite3.connect(
    "data/charging_history.db"
)

totals = calculate_energy_flows(
    conn
)

print()

print("PV kWh:")
print(
    round(
        totals["pv_kwh"],
        2
    )
)

print()

print("Battery kWh:")
print(
    round(
        totals["battery_kwh"],
        2
    )
)

print()

print("Grid kWh:")
print(
    round(
        totals["grid_kwh"],
        2
    )
)

print()

print("EV kWh:")
print(
    round(
        totals["ev_kwh"],
        2
    )
)

print()