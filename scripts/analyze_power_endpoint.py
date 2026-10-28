#!/usr/bin/env python3

import json
from datetime import datetime

INPUT_FILE = "power.json"


def load_json():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load_json()

    ts = data["ts"]
    solar = data["solar"]
    battery = data["battery"]
    grid = data["grid"]
    ev = data["evCharge"]
    soc = data["soc"]

    print("=" * 80)
    print("POWER ENDPOINT ANALYSIS")
    print("=" * 80)

    print(f"Samples        : {len(ts)}")
    print(f"Start          : {ts[0]}")
    print(f"End            : {ts[-1]}")

    print()

    print(f"Max Solar      : {max(solar):.0f} W")
    print(f"Max EV Charge  : {max(ev):.0f} W")

    print(f"Max SOC        : {max(soc):.1f}%")
    print(f"Min SOC        : {min(soc):.1f}%")

    print()

    charging_events = 0
    discharging_events = 0

    for b in battery:
        if b < -50:
            charging_events += 1
        elif b > 50:
            discharging_events += 1

    print(f"Battery charging samples    : {charging_events}")
    print(f"Battery discharging samples : {discharging_events}")

    print()
    print("=" * 80)
    print("EV CHARGING PERIODS")
    print("=" * 80)

    in_session = False
    start = None

    for i in range(len(ts)):

        active = ev[i] > 500

        if active and not in_session:
            in_session = True
            start = ts[i]

        elif not active and in_session:
            end = ts[i]
            in_session = False

            print(f"{start} --> {end}")

    print()

    print("=" * 80)
    print("BATTERY CHARGE MOMENTS")
    print("=" * 80)

    for i in range(len(ts)):

        if 