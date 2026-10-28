import sqlite3


def get_connection(db_path):

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn


def initialize_database(conn):

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        start_time TEXT UNIQUE,
        end_time TEXT,
        duration_minutes REAL,
        kwh REAL,
        avg_price REAL,
        market_cost REAL,
        actual_cost REAL,
        savings REAL,
        imported_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS battery_lots (
        id INTEGER PRIMARY KEY,

        timestamp TEXT,

        source TEXT,

        kwh REAL,

        remaining_kwh REAL,

        cost_per_kwh REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS power_snapshots (
        timestamp TEXT PRIMARY KEY,

        solar_w REAL,
        battery_w REAL,
        grid_w REAL,

        ev_w REAL,
        load_w REAL,

        soc REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS session_energy_breakdown (
        session_id INTEGER PRIMARY KEY,

        pv_direct_kwh REAL,
        battery_kwh REAL,
        grid_direct_kwh REAL,

        actual_cost REAL,

        FOREIGN KEY(session_id)
        REFERENCES sessions(id)
    )
    """)

    conn.commit()


def upgrade_database(conn):

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

    try:
        cur.execute(
            "ALTER TABLE sessions ADD COLUMN actual_cost REAL"
        )
    except:
        pass

    try:
        cur.execute(
            "ALTER TABLE sessions ADD COLUMN savings REAL"
        )
    except:
        pass

    cur.execute("""
    CREATE TABLE IF NOT EXISTS battery_lots (
        id INTEGER PRIMARY KEY,

        timestamp TEXT,

        source TEXT,

        kwh REAL,

        remaining_kwh REAL,

        cost_per_kwh REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS power_snapshots (
        timestamp TEXT PRIMARY KEY,

        solar_w REAL,
        battery_w REAL,
        grid_w REAL,

        ev_w REAL,
        load_w REAL,

        soc REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS session_energy_breakdown (
        session_id INTEGER PRIMARY KEY,

        pv_direct_kwh REAL,
        battery_kwh REAL,
        grid_direct_kwh REAL,

        actual_cost REAL,

        FOREIGN KEY(session_id)
        REFERENCES sessions(id)
    )
    """)

    conn.commit()