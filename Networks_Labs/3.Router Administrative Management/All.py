from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.254",
    "username": "User3",
    "password": "Pass@123",
    "secret": "12345678",
}


def check_ssh(conn):
    try:
        output = conn.send_command("show ip ssh")

        if "SSH Enabled" in output and "version 2" in output:
            return True, "SSH v2 enabled"

        return False, "SSH disabled"

    except:
        return False, "Unable to verify SSH"


def check_rsa_keys(conn):
    try:
        output = conn.send_command(
            "show crypto key mypubkey rsa"
        )

        if "Key name" in output:
            return True, "RSA keys present"

        return False, "RSA keys missing"

    except:
        return False, "Unable to verify RSA keys"


def check_local_users(conn):

    output = conn.send_command(
        "show running-config | include ^username"
    )

    if output.strip():
        return True, "Local users configured"

    return False, "No local users found"


def check_vty_authentication(conn):

    output = conn.send_command(
        "show running-config | section line vty"
    )

    if "login local" in output:
        return True, "VTY uses local authentication"

    return False, "VTY not using login local"


def check_telnet_disabled(conn):

    output = conn.send_command(
        "show running-config | section line vty"
    )

    if "transport input ssh" in output and "telnet" not in output:
        return True, "Telnet disabled"

    return False, "Telnet enabled"


def check_enable_secret(conn):

    output = conn.send_command(
        "show running-config | include enable secret"
    )

    if "enable secret" in output:
        return True, "Enable secret configured"

    return False, "Enable secret missing"


def check_password_policy(conn):

    output = conn.send_command(
        "show running-config | include security passwords min-length"
    )

    if "security passwords min-length" in output:
        return True, "Password policy configured"

    return False, "Password policy missing"


def check_login_blocking(conn):

    output = conn.send_command(
        "show running-config | include login block-for"
    )

    if "login block-for" in output:
        return True, "Brute-force protection enabled"

    return False, "Brute-force protection missing"


def check_session_timeout(conn):

    output = conn.send_command(
        "show running-config | include exec-timeout"
    )

    if "exec-timeout" in output:
        return True, "Session timeout configured"

    return False, "Session timeout missing"


def check_http_disabled(conn):

    output = conn.send_command(
        "show running-config | include ip http"
    )

    http_disabled = "no ip http server" in output
    https_disabled = "no ip http secure-server" in output

    if http_disabled and https_disabled:
        return True, "HTTP/HTTPS disabled"

    return False, "HTTP service enabled"


try:

    print("\nConnecting to router...\n")

    conn = ConnectHandler(**device)

    print("[OK] Connected")

    conn.enable()

    print("[OK] Enable Mode")
    print(f"Prompt: {conn.find_prompt()}")

    checks = [
        check_ssh,
        check_rsa_keys,
        check_local_users,
        check_vty_authentication,
        check_telnet_disabled,
        check_enable_secret,
        check_password_policy,
        check_login_blocking,
        check_session_timeout,
        check_http_disabled,
    ]

    passed = 0
    failed = 0

    print("\n" + "=" * 60)
    print("CISCO SECURITY AUDIT")
    print("=" * 60)

    for check in checks:

        status, message = check(conn)

        if status:
            print(f"[PASS] {message}")
            passed += 1
        else:
            print(f"[FAIL] {message}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Passed Checks : {passed}")
    print(f"Failed Checks : {failed}")

    score = round((passed / len(checks)) * 100)

    print(f"Security Score: {score}%")
    print("=" * 60)

    conn.disconnect()

except Exception as e:

    print("\nERROR:")
    print(e)
