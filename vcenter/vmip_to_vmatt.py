#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from com.vmware.vcenter.vm_client import CustomAttributes
from com.vmware.vcenter.vm_client import Network
from vmware.vapi.vsphere.client import create_vsphere_client
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

# Connect to vCenter server
client = create_vsphere_client(server="<VCENTER_SERVER_IP>", username="<USERNAME>", password="<PASSWORD>")

# Get the network information of all virtual machines
network = client.vcenter.vm.Network
vms = client.vcenter.VM.list()

# Connect to vCenter server using PyVmomi
si = SmartConnectNoSSL(host="<VCENTER_SERVER_IP>", user="<USERNAME>", pwd="<PASSWORD>")
content = si.RetrieveContent()

# Define the custom attribute key and category
attribute_key = "ip_address"
category_name = "Custom Attributes"

# Get the category ID
category_id = None
category_list = client.vcenter.vm_customization.Spec.list_categories()
for category in category_list:
    if category.name == category_name:
        category_id = category.category_id
        break

if category_id is None:
    print(f"Custom attribute category '{category_name}' not found")
    exit()

# Iterate through all virtual machines and set their IP addresses as custom attributes
for vm in vms:
    vm_name = vm.name
    ip_address = None
    for nic_info in network.list(vm.vm):
        if nic_info.nic_type == "VMXNET3":
            nic = nic_info.nic
            if nic.backing.network_type == "STANDARD_PORTGROUP":
                ip_address = nic.ip_address.ip_address
    if ip_address:
        vm_object = content.searchIndex.FindByUuid(None, vm.vm, True, False)
        if vm_object is None:
            print(f"Virtual machine '{vm_name}' not found")
            continue
        else:
            print(f"Setting custom attribute '{attribute_key}' to '{ip_address}' for virtual machine '{vm_name}'")
            custom_attributes = CustomAttributes(client)
            spec = CustomAttributes.CreateSpec(category_id=category_id, key=attribute_key, value=ip_address)
            custom_attributes.create(vm_object, spec)

# Disconnect from vCenter server using PyVmomi
Disconnect(si)
