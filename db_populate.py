#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
from app import db, models

input_xml = sys.argv[1]

tree = ET.parse(input_xml)
systems = tree.getroot()

# get host info
for device in systems:
    # get the attributes
    device_attribs = device.attrib

    # initialize a new System object
    db_device = models.System()

    # populate object with data
    db_device.host_name = device_attribs["host_name"]
    db_device.host_type = device_attribs["host_type"]
    db_device.host_ip = device_attribs["host_ip"]
    db_device.host_location = device_attribs["host_location"]
    db_device.sp_name = device_attribs["sp_name"]
    db_device.sp_ip = device_attribs["sp_ip"]
    db_device.console_cmd = device_attribs["console_cmd"]
    db_device.console_name = device_attribs["console_name"]
    
    if "apc_url" in device_attribs:
        db_device.apc_url = device_attribs["apc_url"]

    if "apc_user" in device_attribs:
        db_device.apc_user = device_attribs["apc_user"]

    if "apc_passwd" in device_attribs:
        db_device.apc_passwd = device_attribs["apc_passwd"]

    db.session.add(db_device)
    db.session.commit()






