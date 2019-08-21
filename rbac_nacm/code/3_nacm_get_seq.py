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
import xmltodict
from getpass import getpass
import time
from jinja2 import Template

# Define variables based on user input.
device = {
    "address": input("Device IP Address?\n"),
    "acl": input("ACL Name?\n"),
    "seq": input("ACE SEQ Number?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

# Raise exception if values are not specified
if None in device.values():
    raise Exception("Missing value.")

# Read in Jinja template
with open("nacm_get_seq.j2") as f:
    template_in = Template(f.read())

# Render Jinja template with variables
filter = template_in.render(acl_name=device["acl"], ace_number=device["seq"])

# Create a loop for sending multiple get requests
for i in range(5):

    """
    Main method that prints netconf capabilities of remote device.
    """
    # Create a NETCONF session to the router with ncclient
    with manager.connect(
            host=device["address"],
            port=830,
            username=device["username"],
            password=device["password"],
            hostkey_verify=False
    ) as m:

        # Retrieve the configuraiton and operation data
        results = m.get(filter)

        # Process the results
        acl_desc = xmltodict.parse(results.xml)["rpc-reply"]["data"]
        acl_match = acl_desc["access-lists"]["access-list"]["access-list-entries"]["access-list-entry"]

        print(" For SEQ number: {}".format(acl_match["rule-name"]["#text"])
              + " the number of ACE matches is: {}".format(acl_match["access-list-entries-oper-data"]["match-counter"]))

        # Small pause to allow YANG to update data store.
        time.sleep(5)