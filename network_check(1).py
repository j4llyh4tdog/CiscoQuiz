"""network_check.py - Check whether inventory devices are UP or DOWN.

Usage:
    python network_check.py            # simulate (uses simulated_status)
    python network_check.py --live     # real TCP connection test to each device
"""
import argparse
import json
import socket
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
INVENTORY_FILE = BASE / "inventory.json"
OUTPUT_FILE = BASE / "output.json"


def load_inventory(path):
    try:
        with open(path) as f:
            return json.load(f)["devices"]
    except FileNotFoundError:
        sys.exit(f"ERROR: {path} not found.")
    except (json.JSONDecodeError, KeyError) as err:
        sys.exit(f"ERROR: invalid inventory file ({err}).")


def check_live(device, timeout=3):
    """Device is UP if its management TCP port accepts a connection."""
    try:
        with socket.create_connection((device["ip"], device.get("port", 22)), timeout=timeout):
            return "UP"
    except OSError:
        return "DOWN"


def check_simulated(device):
    return device.get("simulated_status", "DOWN").upper()


def main():
    parser = argparse.ArgumentParser(description="Network device UP/DOWN checker")
    parser.add_argument("--live", action="store_true", help="perform real TCP checks")
    args = parser.parse_args()

    devices = load_inventory(INVENTORY_FILE)
    mode = "live" if args.live else "simulated"
    results = []

    print(f"Network check ({mode}) - {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"{'Hostname':<10}{'IP Address':<16}{'Location':<14}{'Status'}")
    print("-" * 46)
    for d in devices:
        try:
            status = check_live(d) if args.live else check_simulated(d)
        except Exception as err:  # keep going if one device misbehaves
            print(f"  warning: {d.get('hostname', '?')}: {err}")
            status = "DOWN"
        print(f"{d['hostname']:<10}{d['ip']:<16}{d['location']:<14}{status}")
        results.append({"hostname": d["hostname"], "ip": d["ip"],
                        "location": d["location"], "status": status})

    up = sum(r["status"] == "UP" for r in results)
    print(f"\nSummary: {up} UP, {len(results) - up} DOWN")

    report = {"checked_at": datetime.now().isoformat(timespec="seconds"),
              "mode": mode, "results": results}
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Results saved to {OUTPUT_FILE.name}")
    except OSError as err:
        sys.exit(f"ERROR: could not write output: {err}")


if __name__ == "__main__":
    main()
