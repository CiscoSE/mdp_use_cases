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

from ncclient import manager, xml_
from jinja2 import Template
import yaml

# Reading in Device Details
print("Reading in Device Device Details")
with open("code/device_details.yaml") as f:
    device_details = yaml.safe_load(f.read())

# Reading in Prefix-List Jinja Template
print("Setting Up NETCONF Templates")
with open("code/templates/create_prefix_list.j2") as f:
    prefix_list_template = Template(f.read())

# Reading in Route-Map Jinja Template
with open("code/templates/create_route_map.j2") as f:
    route_map_template = Template(f.read())

print("Creating Device Configurations")

for device in device_details["devices"]:
    print("Defining netmiko session details on DEVICE: {}".format(device["name"]))

    with manager.connect(host=device["ip"],
                         username=device["username"],
                         password=device["password"],
                         allow_agent=False,
                         look_for_keys=False,
                         hostkey_verify=False) as m:

        # Rendering Jinja Template with prefix-list details
        print("Creating Prefix List Configurations from Template")
        with open("code/configs/{}_prefixlist.cfg".format(device["name"]), "w") as f:
            prefix_config = prefix_list_template.render(name=device["prefix_name"], prefixes=device["prefixes"])
            f.write(prefix_config)

        # Rendering Jinja Template with route-map details
        with open("code/configs/{}_routemap.cfg".format(device["name"]), "w") as f:
            map_config = route_map_template.render(name=device["route_map"]["name"],
                                                   entries=device["route_map"]["map_seq"])
            f.write(map_config)

        # Sending XML payload with ncclinent
        print("Sending Prefix List Configuration with Ncclient")
        prefix_resp = m.edit_config(prefix_config, target='running')

        # Sending XML payload with ncclinent
        print("Sending Route-Map Configuration with Ncclient")
        map_resp = m.edit_config(map_config, target='running')
