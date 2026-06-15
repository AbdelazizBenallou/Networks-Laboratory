from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "172.16.1.253",
    "username": "Carlos_John",
    "password": "784512963",
    "secret": "71374572" 
}

print("\nConnecting...\n")

conn = ConnectHandler(**device)
print("Connecting Successful .....")

running_config = conn.send_command("show running-config")

checks = {
    "Local user authentication": "login local",
    "Password encryption": "service password-encryption",
    "Enable secret": "enable secret",
    "SSH version 2": "ip ssh version 2",
    "SSH only on VTY": "transport input ssh",
    "Brute-force protection": "login block-for",
    "Login success logging": "login on-success log",
    "Login failure logging": "login on-failure log",
    "Session timeout": "exec-timeout",
    "HTTP server disabled": "no ip http server",
    "HTTPS server disabled": "no ip http secure-server",
    "DNS lookup disabled": "no ip domain-lookup",
    "Domain name configured": "ip domain-name",
    "Local username exists": "username ",
}

print("=" * 60)
print("ROUTER SECURITY AUDIT")
print("=" * 60)

missing = []

for check_name, pattern in checks.items():
    if pattern in running_config:
        print(f"[OK]   {check_name}")
    else:
        print(f"[FAIL] {check_name}")
        missing.append(check_name)

print("\n" + "=" * 60)

if missing:
    print("MISSING CONFIGURATIONS:")
    for item in missing:
        print(f" - {item}")
else:
    print("All security controls are present.")

print("=" * 60)

conn.disconnect()
