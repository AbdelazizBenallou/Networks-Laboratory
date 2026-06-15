from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.10.254",
    "username": "admin",
    "password": "1234",
}

commands = [
    "interface Loopback1",
    "ip address 3.3.3.3  255.255.255.255",
    "description loopack_interface for ISP-Router"
]

with ConnectHandler(**device) as conn:
    output = conn.send_config_set(commands)
    print(output)
