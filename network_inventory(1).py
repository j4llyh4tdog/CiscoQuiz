"""network_inventory.py - Simple Cisco network device inventory."""

devices = [
    {"hostname": "R1-HQ",   "ip": "192.168.10.1", "type": "Cisco ISR 4331 Router",       "location": "Headquarters", "status": "up"},
    {"hostname": "SW1-HQ",  "ip": "192.168.10.2", "type": "Cisco Catalyst 9300 Switch",  "location": "Headquarters", "status": "up"},
    {"hostname": "R2-BR1",  "ip": "192.168.20.1", "type": "Cisco CSR1000v Router",       "location": "Branch 1",     "status": "down"},
    {"hostname": "SW2-BR1", "ip": "192.168.20.2", "type": "Cisco Catalyst 3850 Switch",  "location": "Branch 1",     "status": "up"},
]


def display_devices(device_list, title):
    print(f"\n=== {title} ===")
    print(f"{'Hostname':<10}{'IP Address':<16}{'Device Type':<30}{'Location':<14}{'Status':<6}")
    print("-" * 76)
    for d in device_list:
        print(f"{d['hostname']:<10}{d['ip']:<16}{d['type']:<30}{d['location']:<14}{d['status'].upper():<6}")
    if not device_list:
        print("(no devices)")


def get_up_devices(device_list):
    return [d for d in device_list if d["status"].lower() == "up"]


def main():
    display_devices(devices, "ALL DEVICES")
    up = get_up_devices(devices)
    display_devices(up, "DEVICES WITH STATUS UP")
    print(f"\nOperational devices: {len(up)} of {len(devices)}")


if __name__ == "__main__":
    main()
