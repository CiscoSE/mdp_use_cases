#!/usr/bin/env python

from ncclient import manager, xml_
from jinja2 import Template
import yaml

print("Reading in Device Device Details")
with open("device_details.yaml") as f:
    device_details = yaml.load(f.read())

print("Setting Up NETCONF Templates")
with open("templates/create_prefix_list.j2") as f:
    prefix_list_template = Template(f.read())

with open("templates/create_route_map.j2") as f:
    route_map_template = Template(f.read())

print("Creating Device Configurations")
# for device in device_details["devices"]:
#     print("Device: {}".format(device["name"]))



for device in device_details["devices"]:
    print("Defining netmiko session details on DEVICE: {}".format(device["name"]))

    with manager.connect(host=device["ip"],
                         username=device["username"],
                         password=device["password"],
                         allow_agent=False,
                         look_for_keys=False,
                         hostkey_verify=False) as m:
        print("Creating Prefix List Configurations from Template")
        with open("configs/{}_prefixlist.cfg".format(device["name"]), "w") as f:
            prefix_config = prefix_list_template.render(name=device["prefix_name"], prefixes=device["prefixes"])
            f.write(prefix_config)

        with open("configs/{}_routemap.cfg".format(device["name"]), "w") as f:
            map_config = route_map_template.render(name=device["route_map"]["name"],
                                                   entries=device["route_map"]["map_seq"])
            f.write(map_config)

        print("Sending Prefix List Configuration with Ncclient")
        prefix_resp = m.edit_config(prefix_config, target='running')

        print("Sending Prefix List Configuration with Ncclient")
        map_resp = m.edit_config(map_config, target='running')
