from battery_daily_ratios import (
    get_daily_battery_ratios
)

ratios = get_daily_battery_ratios(
    "2026-10-22",
    "2026-10-28"
)

print()

for day, ratio in ratios.items():

    print(
        day,
        ratio
    )

print()