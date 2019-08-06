from netmiko import ConnectHandler
from getpass import getpass


# device = {
#     "address": input("Device IP Address?\n"),
#     "username": input("Operator Username?\n"),
#     "password": getpass("Operator Password?\n"),
# }

device = {
    "address": "172.16.30.177",
    "username": "cisco",
    "password": "cisco"
}

# Define netmiko session details and send ping command to router.

for i in range(100):

    with ConnectHandler(device_type='cisco_ios',
                        ip=device["address"],
                        username=device["username"],
                        password=device["password"],
                        port=22) as ch:

        ping_permit = ch.send_command("ping 10.255.255.1 count 10")
        ping_deny = ch.send_command("ping 172.16.11.1 count 10")



