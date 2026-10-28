import sqlite3


def create_battery_lot(
    conn,
    timestamp,
    source,
    kwh,
    cost_per_kwh
):

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO battery_lots (
        timestamp,
        source,
        kwh,
        remaining_kwh,
        cost_per_kwh
    )
    VALUES (
        ?, ?, ?, ?, ?
    )
    """,
    (
        timestamp,
        source,
        kwh,
        kwh,
        cost_per_kwh
    ))

    conn.commit()


def get_open_lots(conn):

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM battery_lots
    WHERE remaining_kwh > 0
    ORDER BY timestamp
    """)

    return cur.fetchall()


def consume_energy(
    conn,
    needed_kwh
):

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    lots = get_open_lots(conn)

    total_cost = 0.0

    remaining = needed_kwh

    for lot in lots:

        if remaining <= 0:
            break

        available = lot["remaining_kwh"]

        take = min(
            available,
            remaining
        )

        total_cost += (
            take *
            lot["cost_per_kwh"]
        )

        new_remaining = (
            available - take
        )

        cur.execute("""
        UPDATE battery_lots
        SET remaining_kwh=?
        WHERE id=?
        """,
        (
            new_remaining,
            lot["id"]
        ))

        remaining -= take

    conn.commit()

    return round(
        total_cost,
        4
    )