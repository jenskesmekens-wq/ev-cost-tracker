import os
import yaml
import json
import requests

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

r = requests.get(
    url,
    headers=client.headers(),
    params={
        "startDate": "2026-10-22",
        "endDate": "2026-10-28",
        "dimension": "day"
    }
)

r.raise_for_status()

data = r.json()

print()

print("selfGeneration")
print(
    data["selfGeneration"]
)

print()

print("battery")
print(
    data["battery"]
)

print()

print("grid")
print(
    data["grid"]
)

print()

print("summary")
print(
    data["summary"]
)

print()