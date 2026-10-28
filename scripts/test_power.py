import os
import yaml

from alphaess_client import (
    AlphaESSClient
)

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

print(data.keys())
print()
print(
    data["ts"][:5]
)