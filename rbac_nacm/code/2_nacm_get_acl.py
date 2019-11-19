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

# Assign user inputs as variables for session establishment
device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

# Raise exception if user did not specify username/password.
if None in device.values():
    raise Exception("Missing username or password.")

# Define filter for retrieving ACL configuration with NETCONF
filter = '''
                <filter>
                  <access-lists xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl-oper">
                    <access-list>
                      <access-control-list-name>IMPACT</access-control-list-name>
                    </access-list>
                  </access-lists>
                  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <ip>
                      <access-list>
                        <extended xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl"/>
                      </access-list>
                    </ip>
                  </native>
                </filter>
         '''

# Define NETCONF session details
with manager.connect(
        host=device["address"],
        port=830,
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
) as m:

    # Retrieve access-list configuration
    results = m.get(filter)

    acl_desc = xmltodict.parse(results.xml)["rpc-reply"]["data"]
    acl_conf = acl_desc["native"]["ip"]["access-list"]["extended"]["access-list-seq-rule"]
    acl_name = acl_desc["access-lists"]["access-list"]
    acl_match = acl_desc["access-lists"]["access-list"]["access-list-entries"]["access-list-entry"]


    # Process the xml data into a readable format.
    print("Access-List Name: {}".format(acl_name["access-control-list-name"]["#text"]))
    for ace in acl_conf:

        try:
            print(" For ACE: {}".format(ace["sequence"]))
            print("  Protocol: {}".format(ace["ace-rule"]["protocol"]))
            print("   Destination Network: {}".format(ace["ace-rule"]["dest-ipv4-address"]))
            print("   Destination Wildcard Mask: {}".format(ace["ace-rule"]["dest-mask"]))
            print("   Source Network: {}".format(ace["ace-rule"]["ipv4-address"]))
            print("   Source Wildcard Mask: {}".format(ace["ace-rule"]["mask"]))
            print("   Action: {}".format(ace["ace-rule"]["action"]))
        except KeyError:
            print("   Action: {}".format(ace["ace-rule"]["action"]))
        except Exception:
            print("  Cannot Understand ACE")

        print("")
