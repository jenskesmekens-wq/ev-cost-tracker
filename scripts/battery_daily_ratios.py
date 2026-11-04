import os
import yaml
import requests

from alphaess_client import AlphaESSClient


def get_daily_battery_ratios(
    start_date,
    end_date
):

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

    url = (
        "https://platform-eur.alphaess.com"
        "/api/internal/v1/sites/"
        "zq6x3eLCpVvbrcEbnLF"
        "/energy"
    )

    r = requests.get(
        url,
        headers=client.headers(),
        params={
            "startDate": start_date,
            "endDate": end_date,
            "dimension": "day"
        }
    )

    r.raise_for_status()

    if not r.text.strip():

        print()
        print(
            "Waarschuwing: lege response "
            "van AlphaESS energy endpoint."
        )
        print(
            "Fallback naar 100% grid."
        )
        print()

        return {}

    try:

        data = r.json()

    except Exception:

        print()
        print(
            "Waarschuwing: ongeldige JSON "
            "van AlphaESS energy endpoint."
        )
        print(
            "Fallback naar 100% grid."
        )
        print()

        return {}

    if not data:

        print()
        print(
            "Waarschuwing: lege data "
            "van AlphaESS energy endpoint."
        )
        print(
            "Fallback naar 100% grid."
        )
        print()

        return {}

    try:

        days = data["ts"]

        pv_to_battery = (
            data["selfGeneration"]["battery"]
        )

        grid_to_battery = (
            data["grid"]["battery"]
        )

    except Exception:

        print()
        print(
            "Waarschuwing: onverwachte "
            "AlphaESS response structuur."
        )
        print(
            "Fallback naar 100% grid."
        )
        print()

        return {}

    ratios = {}

    for i in range(
        len(days)
    ):

        day = days[i]

        pv = pv_to_battery[i]
        grid = grid_to_battery[i]

        total = pv + grid

        if total <= 0:

            ratios[day] = (
                0.0,
                1.0
            )

            continue

        ratios[day] = (
            pv / total,
            grid / total
        )

    return ratios