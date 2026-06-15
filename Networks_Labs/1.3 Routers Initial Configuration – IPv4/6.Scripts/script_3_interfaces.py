from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "172.16.1.253",
    "username": "Carlos_John",
    "password": "784512963",
    "secret": "71374572" 
}

try:
    with ConnectHandler(**device) as conn:

        print("\n=== CURRENT INTERFACES ===\n")
        print(conn.send_command("show ip interface brief | exclude down"))

        interface = input("\nEnter interface name (e.g. FastEthernet0/1): ")
        ip_addr = input("Enter IP address: ")
        mask = input("Enter subnet mask (e.g. 255.255.255.0): ")

        commands = [
            f"interface {interface}",
            f"ip address {ip_addr} {mask}",
            "no shutdown"
        ]

        print("\nApplying configuration...\n")
        output = conn.send_config_set(commands)
        print(output)

        print("\n=== UPDATED INTERFACES ===\n")
        print(conn.send_command("show ip interface brief"))

except Exception as e:
    print(f"\nError: {e}")
