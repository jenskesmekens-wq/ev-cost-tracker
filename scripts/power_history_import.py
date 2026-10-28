import sqlite3


def save_power_snapshot(
    conn,
    timestamp,
    solar_w,
    battery_w,
    grid_w,
    ev_w,
    load_w,
    soc
):

    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO power_snapshots (
        timestamp,
        solar_w,
        battery_w,
        grid_w,
        ev_w,
        load_w,
        soc
    )
    VALUES (
        ?, ?, ?, ?, ?, ?, ?
    )
    """,
    (
        timestamp,
        solar_w,
        battery_w,
        grid_w,
        ev_w,
        load_w,
        soc
    ))

    conn.commit()