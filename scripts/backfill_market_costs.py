import sqlite3

from datetime import datetime

from history_price_loader import (
    load_day_prices
)

from cost_engine import (
    get_quarter_prices,
    calculate_session_market_price
)


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

cur.execute("""
SELECT
 id,
 start_time,
 end_time,
 kwh
FROM sessions
""")

rows = cur.fetchall()

updated = 0

for row in rows:

    start = datetime.fromisoformat(
        row["start_time"].replace(
            " ",
            "T"
        )
    )

    end = datetime.fromisoformat(
        row["end_time"].replace(
            " ",
            "T"
        )
    )

    day = start.strftime(
        "%Y-%m-%d"
    )

    data = load_day_prices(day)

    if not data:
        continue

    lookup = get_quarter_prices(data)

    avg_price, market_cost = (
        calculate_session_market_price(
            start,
            end,
            row["kwh"],
            lookup
        )
    )

    cur.execute("""
    UPDATE sessions
    SET
      avg_price=?,
      market_cost=?
    WHERE id=?
    """,
    (
        avg_price,
        market_cost,
        row["id"]
    ))

    updated += 1

conn.commit()

print()

print(
    f"{updated} sessies bijgewerkt"
)

print()