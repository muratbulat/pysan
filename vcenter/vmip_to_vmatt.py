#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

# Connect to vCenter server
si = SmartConnect(host="<VCENTER_SERVER_IP>", user="<USERNAME>", pwd="<PASSWORD>")

# Get all VMs
vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vms = vm_view.view

# Loop through each VM
for vm in vms:
  # Get the network adapter info from the annotation
  ip_address=None
  ip_address=vm.guest.ipAddress
  # Set the IP address as an attribute of the VM, if it exists
  if vm.guest.ipAddress != None:
    if vm.GetCustomValue("IP Address") == None:
      vm.SetCustomValue("IP Address", ip_address)
      print(vm.name, "Sanal sunucu attribute ip bilgisine", ip_address, "yazıldı")
    else:
      print(vm.name, "Sanal sunucu attribute ip bilgisi zaten mevcut")
  else:
    print(vm.name, "Sanal sunucu ip bilgisi yok")

# Disconnect from vCenter server
Disconnect(si)
