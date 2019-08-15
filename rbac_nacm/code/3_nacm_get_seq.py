#!/usr/bin/env python

from ncclient import manager
import sys
import xml.dom.minidom
import xmltodict
from getpass import getpass
import time
from jinja2 import Template

device = {
    "address": input("Device IP Address?\n"),
    "acl": input("ACL Name?\n"),
    "seq": input("ACE SEQ Number?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),

}

with open("nacm_get_seq.j2") as f:
    template_in = Template(f.read())

filter = template_in.render(acl_name=device["acl"], ace_number=device["seq"])


if None in device.values():
    raise Exception("Missing username or password.")

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


        acl_desc = xmltodict.parse(results.xml)["rpc-reply"]["data"]
        acl_match = acl_desc["access-lists"]["access-list"]["access-list-entries"]["access-list-entry"]


        print(" For SEQ number: {}".format(acl_match["rule-name"]["#text"])
              + " the number of ACE matches is: {}".format(acl_match["access-list-entries-oper-data"]["match-counter"]))

        time.sleep(5)
