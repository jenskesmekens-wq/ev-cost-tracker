import os
import yaml
import json

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

url = (
    "https://platform-eur.alphaess.com"
    "/api/internal/v1/sites/"
    "zq6x3eLCpVvbrcEbnLF"
    "/energy"
)

import requests

r = requests.get(
    url,
    headers=client.headers(),
    params={
        "startDate": "2026-10-28",
        "endDate": "2026-10-28",
        "dimension": "day"
    }
)

r.raise_for_status()

data = r.json()

print()

print(data.keys())

print()

print(
    json.dumps(
        data,
        indent=2
    )[:3000]
)

print()

print()

print(
    "Aantal tsHour:",
    len(data["tsHour"])
)

print()

print(
    data["tsHour"][:10]
)
