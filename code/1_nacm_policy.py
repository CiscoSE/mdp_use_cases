#! /usr/bin/env python

import os
from ncclient import manager
import xmltodict
from getpass import getpass
from xml.dom import minidom

device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

if None in device.values():
    raise Exception("Missing username or password.")

filter = """
<filter>
  <nacm xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-acm" />
</filter>
"""

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

with manager.connect(
        host=device["address"],
        port=830,
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
) as m:

    # Get current NACM
    r = m.get(filter)
    print("Current NACM Configuration.")
    xml_doc = minidom.parseString(r.xml)
    print(xml_doc.toprettyxml(indent="  "))
    print("")

    # Add new rules
    print("Configuring NACM Rule to allow PRIV01 to GET")
    r = m.edit_config(target="running", config=data)
    print("NETCONF RPC OK: {}".format(r.ok))