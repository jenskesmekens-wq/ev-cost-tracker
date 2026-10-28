import sqlite3

def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY,start_time TEXT UNIQUE,end_time TEXT,duration_minutes REAL,kwh REAL,avg_price REAL,market_cost REAL,actual_cost REAL,savings REAL,imported_at TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS battery_lots (id INTEGER PRIMARY KEY,timestamp TEXT,source TEXT,kwh REAL,remaining_kwh REAL,cost_per_kwh REAL)""")
    conn.commit()
