import os
import yaml
import sqlite3

from alphaess_client import AlphaESSClient


with open(
    "config.yaml",
    encoding="utf-8"
) as f:

    cfg = yaml.safe_load(f)


client = AlphaESSClient(
    cfg["alphaess"]["email"],
    os.getenv(
        "ALPHAESS_PASSWORD"
    )
)

client.login()

data = client.get_power_history(
    "2026-10-27T23:00:00Z",
    "2026-10-28T22:59:59Z",
    5
)

conn = sqlite3.connect(
    "data/charging_history.db"
)

cur = conn.cursor()

count = 0

for i in range(len(data["ts"])):

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
        data["ts"][i],
        data["solar"][i],
        data["battery"][i],
        data["grid"][i],
        data["evCharge"][i],
        data["load"][i],
        data["soc"][i]
    ))

    count += 1

conn.commit()

print()

print(
    f"{count} snapshots opgeslagen"
)

print()