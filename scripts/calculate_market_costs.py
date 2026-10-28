import sqlite3
import requests

from datetime import datetime

from cost_engine import (
    get_quarter_prices,
    calculate_session_market_price
)


PRICE_URL = (
    "https://jenskesmekens-wq.github.io/"
    "Energieprijs-v4/prices.json"
)


conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

try:
    cur.execute(
        "ALTER TABLE sessions ADD COLUMN avg_price REAL"
    )
except:
    pass

try:
    cur.execute(
        "ALTER TABLE sessions ADD COLUMN market_cost REAL"
    )
except:
    pass

print("Prijzen ophalen...")

price_data = requests.get(
    PRICE_URL,
    timeout=30
).json()

price_lookup = get_quarter_prices(
    price_data
)

cur.execute(
    """
    SELECT
        id,
        start_time,
        end_time,
        kwh
    FROM sessions
    """
)

rows = cur.fetchall()

for row in rows:

    start_time = datetime.fromisoformat(
        row["start_time"].replace(" ", "T")
    )

    end_time = datetime.fromisoformat(
        row["end_time"].replace(" ", "T")
    )

    avg_price, market_cost = (
        calculate_session_market_price(
            start_time,
            end_time,
            row["kwh"],
            price_lookup
        )
    )

    cur.execute(
        """
        UPDATE sessions
        SET
            avg_price = ?,
            market_cost = ?
        WHERE id = ?
        """,
        (
            avg_price,
            market_cost,
            row["id"]
        )
    )

conn.commit()

print(
    f"{len(rows)} sessies berekend."
)

print("Klaar.")