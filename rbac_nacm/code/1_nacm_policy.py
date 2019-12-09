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
from getpass import getpass
from xml.dom import minidom

# Assign user inputs as variables for session establishment
device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

# Raise exception if inputs were not specified.
if None in device.values():
    raise Exception("Missing username or password.")

# Filter for retrieving current NACM config.
filter = """
<filter>
  <nacm xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-acm" />
</filter>
"""

# Define filter for restricting users at PRIV02 from editing configuration.
data = """
<config>
  <nacm xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-acm">
    <rule-list>
      <name>only-get</name>
      <group>PRIV02</group>
      <rule>
        <name>deny-edit-config</name>
        <module-name>ietf-netconf</module-name>
        <rpc-name>edit-config</rpc-name>
        <access-operations>exec</access-operations>
        <action>deny</action>
      </rule>
      <rule>
        <name>allow-get</name>
        <module-name>ietf-netconf</module-name>
        <rpc-name>get</rpc-name>
        <access-operations>exec</access-operations>
        <action>permit</action>
      </rule>
      <rule>
        <name>allow-models</name>
        <module-name>*</module-name>
        <access-operations>read</access-operations>
        <action>permit</action>
      </rule>
    </rule-list>
  </nacm>
</config>
  """

# Define NETCONF session details
with manager.connect(
        host=device["address"],
        port=830,
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
) as m:

    # Get current NACM
    r = m.get(filter)
    print("NACM Configuration Before Defining PRIV02 Policy.")
    xml_doc = minidom.parseString(r.xml)
    print(xml_doc.toprettyxml(indent="  "))
    print("")

    # Add new rules
    print("Configuring NACM Rule to allow PRIV02 to GET")
    r = m.edit_config(target="running", config=data)
    print("NETCONF RPC OK: {}".format(r.ok))
    print("")

    # Display NACM after making the changes
    r = m.get(filter)
    print("NACM Configuration After Defining PRIV02 Policy.")
    xml_doc = minidom.parseString(r.xml)
    print(xml_doc.toprettyxml(indent="  "))
    print("")
