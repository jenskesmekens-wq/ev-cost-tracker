import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent


def run(script_name):

    print()
    print("=" * 60)
    print(script_name)
    print("=" * 60)
    print()

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / script_name)
        ]
    )

    if result.returncode != 0:

        raise RuntimeError(
            f"{script_name} failed"
        )


def main():

    run("session_sync.py")

    run("update_price_history.py")

    run("import_power_history_full.py")

    run("calculate_market_costs.py")

    run("session_energy_allocation.py")

    run("calculate_actual_cost_v2.py")

    run("generate_dashboard_json.py")

    print()
    print("=" * 60)
    print("UPDATE COMPLETED")
    print("=" * 60)
    print()


if __name__ == "__main__":

    main()