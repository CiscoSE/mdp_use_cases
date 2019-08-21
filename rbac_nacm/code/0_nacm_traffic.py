#!/usr/bin/env python

"""

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Bryan Byrne <brybyrne@cisco.com>"
__contributors__ = [
]
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"

from netmiko import ConnectHandler
from getpass import getpass

# Assign user inputs as variables for session establishment
device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

# Define netmiko session details and send ping command to router.
for i in range(100):

    with ConnectHandler(device_type='cisco_ios',
                        ip=device["address"],
                        username=device["username"],
                        password=device["password"],
                        port=22) as ch:

        ping_permit = ch.send_command("ping 10.255.255.1")
        ping_deny = ch.send_command("ping 172.16.11.1")

        print(ping_deny)
        print(ping_permit)