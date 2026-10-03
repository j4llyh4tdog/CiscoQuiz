"""interface_automation.py - Configure Loopback100 via RESTCONF and verify it."""
import json
import requests
import urllib3

ROUTER_IP = "192.168.10.1"
USERNAME = "admin"
PASSWORD = "Cisco123!"
INTERFACE = "Loopback100"
URL = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces/interface={INTERFACE}"
HEADERS = {"Accept": "application/yang-data+json",
           "Content-Type": "application/yang-data+json"}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PAYLOAD = {
    "ietf-interfaces:interface": {
        "name": INTERFACE,
        "description": "STUDENT-AUTOMATION",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [{"ip": "10.100.100.1", "netmask": "255.255.255.255"}]
        },
    }
}


def configure():
    """PUT creates or replaces the interface (idempotent). 201=created, 204=replaced."""
    print(f"PUT {URL}\nPayload:\n{json.dumps(PAYLOAD, indent=2)}")
    try:
        r = requests.put(URL, auth=(USERNAME, PASSWORD), headers=HEADERS,
                         data=json.dumps(PAYLOAD), verify=False, timeout=10)
    except requests.exceptions.RequestException as err:
        print(f"CONFIGURATION FAILED: {err}")
        return False
    print(f"HTTP Status Code: {r.status_code}")
    if r.status_code in (201, 204):
        print(f"CONFIGURATION SUCCEEDED ({'created' if r.status_code == 201 else 'updated'})")
        return True
    print(f"CONFIGURATION FAILED: {r.text}")
    return False


def verify():
    print(f"\nVerifying {INTERFACE}...")
    try:
        r = requests.get(URL, auth=(USERNAME, PASSWORD), headers=HEADERS,
                         verify=False, timeout=10)
    except requests.exceptions.RequestException as err:
        print(f"VERIFICATION FAILED: {err}")
        return
    print(f"HTTP Status Code: {r.status_code}")
    if r.status_code != 200:
        print(f"VERIFICATION FAILED: {r.text}")
        return
    intf = r.json().get("ietf-interfaces:interface", {})
    addr = intf.get("ietf-ip:ipv4", {}).get("address", [{}])[0]
    checks = {
        "Description": (intf.get("description"), "STUDENT-AUTOMATION"),
        "IP Address":  (addr.get("ip"), "10.100.100.1"),
        "Netmask":     (addr.get("netmask"), "255.255.255.255"),
        "Enabled":     (intf.get("enabled"), True),
    }
    ok = True
    for name, (actual, expected) in checks.items():
        match = actual == expected
        ok &= match
        print(f"  {name:<12}: {actual}  [{'OK' if match else 'MISMATCH, expected ' + str(expected)}]")
    print("VERIFICATION PASSED" if ok else "VERIFICATION FAILED")


if __name__ == "__main__":
    if configure():
        verify()
