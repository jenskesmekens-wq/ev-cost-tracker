import sqlite3


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

cur.execute("""
SELECT

    s.id,
    s.kwh,
    s.market_cost,

    b.pv_direct_kwh,
    b.battery_kwh,
    b.grid_direct_kwh

FROM sessions s

JOIN session_energy_breakdown b
ON s.id = b.session_id
""")

rows = cur.fetchall()

updated = 0

for row in rows:

    total_supply = (
        (row["pv_direct_kwh"] or 0) +
        (row["battery_kwh"] or 0) +
        (row["grid_direct_kwh"] or 0)
    )

    if total_supply <= 0:
        continue

    grid_ratio = (
        row["grid_direct_kwh"] /
        total_supply
    )

    actual_cost = (
        row["market_cost"] *
        grid_ratio
    )

    savings = (
        row["market_cost"] -
        actual_cost
    )

    cur.execute("""
    UPDATE sessions
    SET
        actual_cost = ?,
        savings = ?
    WHERE id = ?
    """,
    (
        round(actual_cost, 2),
        round(savings, 2),
        row["id"]
    ))

    updated += 1

conn.commit()

print()

print(
    f"{updated} sessies bijgewerkt"
)

print()
