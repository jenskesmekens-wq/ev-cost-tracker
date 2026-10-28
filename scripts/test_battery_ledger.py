import sqlite3

from battery_ledger import *

conn = sqlite3.connect(
    "data/charging_history.db"
)

create_battery_lot(
    conn,
    "2026-10-28 01:00",
    "GRID",
    2.0,
    0.10
)

create_battery_lot(
    conn,
    "2026-10-28 02:00",
    "PV",
    3.0,
    0.0
)

cost = consume_energy(
    conn,
    4.0
)

print()

print(
    "Consumed cost:",
    cost
)

print()