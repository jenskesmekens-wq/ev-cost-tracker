import sqlite3

from stats import get_month_stats


conn = sqlite3.connect(
    "data/charging_history.db"
)

stats = get_month_stats(conn)

print()

print("EV COST TRACKER")

print("--------------------")

print()

print(
    f"Aantal sessies : {stats['sessions']}"
)

print(
    f"Totaal kWh     : {stats['total_kwh']}"
)

print(
    f"Totale kost    : €{stats['total_cost']}"
)

print(
    f"Gem €/kWh      : €{stats['avg_price']}"
)

print()