from pathlib import Path
from datetime import datetime

import sqlite3
import yaml
import os

from alphaess_client import AlphaESSClient


ROOT = Path(__file__).resolve().parent.parent

CONFIG = ROOT / "config.yaml"

START_DATE = datetime(2026, 10, 15)


def load_config():

    with open(
        CONFIG,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)


def get_database_path(cfg):

    db_path = (
        ROOT /
        cfg["database"]["path"]
    )

    db_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return str(db_path)


def main():

    cfg = load_config()

    email = os.getenv(
        "ALPHAESS_EMAIL",
        cfg["alphaess"]["email"]
    )

    password = os.getenv(
        "ALPHAESS_PASSWORD",
        ""
    )

    print()
    print(
        f"Email: {email}"
    )
    print(
        f"Password gevuld: {bool(password)}"
    )
    print(
        f"Password lengte: {len(password)}"
    )
    print()

    client = AlphaESSClient(
        email,
        password
    )

    client.login()

    sessions = client.get_charging_sessions(
        cfg["system"]["sys_sn"],
        cfg["system"]["charger_sn"]
    )

    conn = sqlite3.connect(
        get_database_path(cfg)
    )

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (

        id INTEGER PRIMARY KEY,

        start_time TEXT UNIQUE,
        end_time TEXT,

        kwh REAL
    )
    """)

    inserted_count = 0
    updated_count = 0

    for s in sessions:

        st = datetime.fromisoformat(
            s["beginDate"]
            .replace(" ", "T")
        )

        if st < START_DATE:
            continue

        c.execute(
            """
            SELECT
                end_time,
                kwh
            FROM sessions
            WHERE start_time = ?
            """,
            (
                s["beginDate"],
            )
        )

        existing = c.fetchone()

        if existing is None:

            c.execute(
                """
                INSERT INTO sessions (

                    start_time,
                    end_time,
                    kwh

                )
                VALUES (
                    ?, ?, ?
                )
                """,
                (
                    s["beginDate"],
                    s["endDate"],
                    s["chargingCapacity"]
                )
            )

            inserted_count += 1

        else:

            old_end_time = existing[0]
            old_kwh = existing[1]

            new_end_time = s["endDate"]
            new_kwh = s["chargingCapacity"]

            if (
                old_end_time != new_end_time
                or
                old_kwh != new_kwh
            ):

                c.execute(
                    """
                    UPDATE sessions
                    SET
                        end_time = ?,
                        kwh = ?
                    WHERE start_time = ?
                    """,
                    (
                        new_end_time,
                        new_kwh,
                        s["beginDate"]
                    )
                )

                updated_count += 1

    conn.commit()

    print()
    print(
        f"Sessies opgehaald: {len(sessions)}"
    )
    print(
        f"Nieuwe sessies: {inserted_count}"
    )
    print(
        f"Bijgewerkte sessies: {updated_count}"
    )
    print()


if __name__ == "__main__":

    main()