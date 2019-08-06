#!/usr/bin/env python

from ncclient import manager
import sys
import xml.dom.minidom
import xmltodict
from getpass import getpass

device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),
}

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


if None in device.values():
    raise Exception("Missing username or password.")



with manager.connect(
        host=device["address"],
        port=830,
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
) as m:
    results = m.get(filter)

    acl_desc = xmltodict.parse(results.xml)["rpc-reply"]["data"]
    acl_conf = acl_desc["native"]["ip"]["access-list"]["extended"]["access-list-seq-rule"]
    acl_name = acl_desc["access-lists"]["access-list"]
    acl_match = acl_desc["access-lists"]["access-list"]["access-list-entries"]["access-list-entry"]

    print(xml.dom.minidom.parseString(results.xml).toprettyxml())

    # Process the xml data into a readable format.
    print("Access-List Name: {}".format(acl_name["access-control-list-name"]["#text"]))
    for ace in acl_conf:

        try:
            print(" For ACE: {}".format(ace["sequence"]))
            print("  Protocol: {}".format(ace["ace-rule"]["protocol"]))
            print("   Destination Network: {}".format(ace["ace-rule"]["dest-ipv4-address"]))
            print("   Destinaiton Wildcard Mask: {}".format(ace["ace-rule"]["dest-mask"]))
            print("   Source Network: {}".format(ace["ace-rule"]["ipv4-address"]))
            print("   Source Wildcard Mask: {}".format(ace["ace-rule"]["mask"]))
            print("   Action: {}".format(ace["ace-rule"]["action"]))
        except KeyError:
            print("   Action: {}".format(ace["ace-rule"]["action"]))
        except Exception:
            print("  Cannot Understand ACE")

        print("")
