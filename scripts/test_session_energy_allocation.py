import sqlite3

from session_energy_allocation import (
    allocate_session_energy
)

conn = sqlite3.connect(
    "data/charging_history.db"
)

count = allocate_session_energy(
    conn
)

print()

print(
    f"{count} sessies verwerkt"
)

print()

conn.row_factory = sqlite3.Row

cur = conn.cursor()

cur.execute("""
SELECT *
FROM session_energy_breakdown
LIMIT 10
""")

for row in cur.fetchall():

    print(
        dict(row)
    )

print()