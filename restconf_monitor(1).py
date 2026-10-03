"""restconf_monitor.py - Retrieve interface name/enabled status via RESTCONF."""
import requests
import urllib3

ROUTER_IP = "192.168.10.1"
USERNAME = "admin"
PASSWORD = "Cisco123!"
RESOURCE = "/restconf/data/ietf-interfaces:interfaces"
URL = f"https://{ROUTER_IP}{RESOURCE}"
HEADERS = {"Accept": "application/yang-data+json"}

# Lab routers use self-signed certificates; silence the warning for verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    print(f"GET {URL}")
    try:
        response = requests.get(URL, auth=(USERNAME, PASSWORD), headers=HEADERS,
                                verify=False, timeout=10)
    except requests.exceptions.ConnectTimeout:
        print("ERROR: Connection timed out. Is the router reachable?")
        return
    except requests.exceptions.ConnectionError as err:
        print(f"ERROR: Could not connect to {ROUTER_IP}: {err}")
        return
    except requests.exceptions.RequestException as err:
        print(f"ERROR: Request failed: {err}")
        return

    print(f"HTTP Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Request unsuccessful: {response.text}")
        return

    interfaces = response.json().get("ietf-interfaces:interfaces", {}).get("interface", [])
    print(f"\n{'Interface':<25}{'Enabled'}")
    print("-" * 35)
    for intf in interfaces:
        print(f"{intf.get('name', 'N/A'):<25}{intf.get('enabled', 'N/A')}")


if __name__ == "__main__":
    main()
