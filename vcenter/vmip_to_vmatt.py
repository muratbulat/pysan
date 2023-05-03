#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

# Connect to vCenter server
si = SmartConnect(host="<VCENTER_SERVER_IP>", user="<USERNAME>", pwd="<PASSWORD>")

# Get all virtual machines
content = si.RetrieveContent()
vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vms = vm_view.view

# Define the attribute key
attribute_key = "ip_address"

# Iterate through all virtual machines and set their IP addresses as attributes
for vm in vms:
    vm_name = vm.name
    ip_address = None
    for nic in vm.guest.net:
        if nic.network != None:
            ip_address = nic.ipAddress[0]
    if ip_address:
        print(f"Setting attribute '{attribute_key}' to '{ip_address}' for virtual machine '{vm_name}'")
        spec = vim.vm.ConfigSpec()
        spec.extraConfig = [vim.option.OptionValue(key=attribute_key, value=ip_address)]
        vm.ReconfigVM_Task(spec=spec)
        
# Disconnect from vCenter server
Disconnect(si)
