import sqlite3


def get_month_stats(conn):

    cur = conn.cursor()

    cur.execute("""
    SELECT
        COUNT(*) as sessions,
        ROUND(SUM(kwh),2) as total_kwh,
        ROUND(SUM(market_cost),2) as total_cost
    FROM sessions
    """)

    row = cur.fetchone()

    sessions = row[0] or 0
    total_kwh = row[1] or 0
    total_cost = row[2] or 0

    avg_price = 0

    if total_kwh > 0:
        avg_price = round(
            total_cost / total_kwh,
            5
        )

    return {
        "sessions": sessions,
        "total_kwh": total_kwh,
        "total_cost": total_cost,
        "avg_price": avg_price
    }