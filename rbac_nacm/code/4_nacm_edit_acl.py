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

from ncclient import manager
from ncclient.operations.rpc import RPCError
from getpass import getpass
from jinja2 import Template
import yaml
from ncclient.operations import RPCError

# Define variables based on user input.
device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

# Raise exception if values are not specified
if None in device.values():
    raise Exception("Missing value.")

# Read in device details from YAML file
with open("nacm_edit_acl.yaml") as f:
    entries = yaml.safe_load(f.read())

# Read in Jinja template
with open("nacm_edit_acl.j2") as f:
    acl_template = Template(f.read())

# Render template and deploy for ACE entries.
for entry in entries:
    acl_config = acl_template.render(aces=entry["aces"], acl_name=entry["name"])

    # Create a NETCONF session to the router with ncclient
    with manager.connect(
            host=device["address"],
            port=830,
            username=device["username"],
            password=device["password"],
            hostkey_verify=False
    ) as m:

        # Deploy XML payload
        try:
            r = m.edit_config(acl_config, target='running')
        # Raise exception if user does not have correct permissions.
        except RPCError as e:
            # Look for RPC error indicating access denied (or something else)
            print("There was an error ({}) with your transaction.".format(e.tag))
            exit(1)

        # Print OK status
        print("NETCONF RPC OK: {}".format(r.ok))