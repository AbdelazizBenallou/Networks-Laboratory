from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.10.254",
    "username": "admin",
    "password": "1234",
}

try:
    net_connect = ConnectHandler(**device)

    print("Connected Successfully!")
    output = net_connect.send_command("show ip int br | include up")
    print(output)
    net_connect.disconnect()

except Exception as e:
    print("ERROR:", e)
