#!/usr/bin/env python3

import json

INPUT_FILE = "power.json"

BATTERY_THRESHOLD = -100


def load_json():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def classify_source(solar_w, grid_w):

    solar_contrib = max(0, solar_w)

    grid_import = max(0, grid_w)

    if solar_contrib > 100 and grid_import < 100:
        return "PV"

    if grid_import > 100 and solar_contrib < 100:
        return "GRID"

    if solar_contrib > 100 and grid_import > 100:
        return "MIXED"

    return "UNKNOWN"


def main():

    data = load_json()

    ts = data["ts"]
    solar = data["solar"]
    grid = data["grid"]
    battery = data["battery"]
    soc = data["soc"]

    print("=" * 100)
    print("BATTERY CHARGE SOURCE DETECTION")
    print("=" * 100)

    total_pv = 0
    total_grid = 0
    total_mixed = 0

    lot_counter = 0

    for i in range(len(ts)):

        battery_power = battery[i]

        #
        # batterij laden
        #
        if battery_power < BATTERY_THRESHOLD:

            source = classify_source(
                solar[i],
                grid[i]
            )

            #
            # 5 minuten -> kWh
            #
            energy_kwh = abs(battery_power) / 1000 * (5 / 60)

            if source == "PV":
                total_pv += energy_kwh

            elif source == "GRID":
                total_grid += energy_kwh

            elif source == "MIXED":
                total_mixed += energy_kwh

            lot_counter += 1

            print(
                f"{lot_counter:04d} | "
                f"{ts[i]} | "
                f"{source:5s} | "
                f"{energy_kwh:7.3f} kWh | "
                f"Solar={solar[i]:7.0f}W | "
                f"Grid={grid[i]:7.0f}W | "
                f"SOC={soc[i]:5.1f}%"
            )

    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)

    print(f"PV Energy     : {total_pv:.3f} kWh")
    print(f"GRID Energy   : {total_grid:.3f} kWh")
    print(f"MIXED Energy  : {total_mixed:.3f} kWh")

    print()

    total = total_pv + total_grid + total_mixed

    print(f"TOTAL CHARGED : {total:.3f} kWh")


if __name__ == "__main__":
    main()