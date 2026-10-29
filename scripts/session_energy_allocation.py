import sqlite3
from datetime import datetime


def allocate_session_energy(conn):

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

    sessions = cur.fetchall()

    processed = 0

    for session in sessions:

        start_time = datetime.fromisoformat(
            session["start_time"]
            .replace(" ", "T")
        )

        end_time = datetime.fromisoformat(
            session["end_time"]
            .replace(" ", "T")
        )

        cur.execute("""
        SELECT *
        FROM power_snapshots
        """)

        snapshots = cur.fetchall()

        pv_kwh = 0.0
        battery_kwh = 0.0
        grid_kwh = 0.0
        measured_ev = 0.0

        for snap in snapshots:

            snap_time = datetime.fromisoformat(
                snap["timestamp"]
                .replace("Z", "")
            )

            if (
                snap_time < start_time
                or
                snap_time > end_time
            ):
                continue

            ev_w = snap["ev_w"] or 0

            if ev_w <= 0:
                continue

            hours = 5 / 60

            ev_kwh = (
                ev_w * hours
            ) / 1000

            measured_ev += ev_kwh

            solar_w = max(
                0,
                snap["solar_w"] or 0
            )

            battery_w = max(
                0,
                abs(
                    snap["battery_w"] or 0
                )
            )

            grid_w = max(
                0,
                snap["grid_w"] or 0
            )

            total_supply = (
                solar_w +
                battery_w +
                grid_w
            )

            if total_supply <= 0:
                continue

            pv_ratio = (
                solar_w /
                total_supply
            )

            battery_ratio = (
                battery_w /
                total_supply
            )

            grid_ratio = (
                grid_w /
                total_supply
            )

            pv_kwh += (
                ev_kwh *
                pv_ratio
            )

            battery_kwh += (
                ev_kwh *
                battery_ratio
            )

            grid_kwh += (
                ev_kwh *
                grid_ratio
            )

        #
        # Normaliseren naar
        # de officiële kWh van de laadpaal
        #

        if measured_ev > 0:

            factor = (
                session["kwh"] /
                measured_ev
            )

            pv_kwh *= factor
            battery_kwh *= factor
            grid_kwh *= factor

        cur.execute("""
        INSERT OR REPLACE
        INTO session_energy_breakdown (

            session_id,

            pv_direct_kwh,
            battery_kwh,
            grid_direct_kwh,

            actual_cost

        )
        VALUES (
            ?, ?, ?, ?, ?
        )
        """,
        (
            session["id"],

            round(
                pv_kwh,
                3
            ),

            round(
                battery_kwh,
                3
            ),

            round(
                grid_kwh,
                3
            ),

            None
        ))

        processed += 1

    conn.commit()

    return processed