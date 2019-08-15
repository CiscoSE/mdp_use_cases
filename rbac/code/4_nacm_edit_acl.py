#!/usr/bin/env python

from ncclient import manager
from ncclient.operations.rpc import RPCError
from getpass import getpass
from jinja2 import Template
import yaml
from ncclient.operations import RPCError

device = {
    "address": input("Device IP Address?\n"),
    "username": input("Operator Username?\n"),
    "password": getpass("Operator Password?\n"),


}


with open("nacm_edit_acl.yaml") as f:
    entries = yaml.safe_load(f.read())

with open("nacm_edit_acl.j2") as f:
    acl_template = Template(f.read())

for entry in entries:
    acl_config = acl_template.render(aces=entry["aces"], acl_name=entry["name"])

    with manager.connect(
            host=device["address"],
            port=830,
            username=device["username"],
            password=device["password"],
            hostkey_verify=False
    ) as m:

        try:
            r = m.edit_config(acl_config, target='running')
        except RPCError as e:
            # Look for RPC error indicating access denied (or something else)
            print("There was an error ({}) with your transaction.".format(e.tag))
            exit(1)

        # Print OK status
        print("NETCONF RPC OK: {}".format(r.ok))








