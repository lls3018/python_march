#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program for listing the vms on an ESX / vCenter host
"""
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from pyVmomi import vim
from ServerClient import VsphereClient


def get_network_type(network):
   return ('distributed port group' if network['switch_distributed']
           else 'port group')


def get_network_name(network):
   if 'name' in network:
      net_name = network['name']
   return net_name


def get_vswitches(self):
   # We only want to list vswitches that are on all hosts, as we will try
   # to create port groups on the same vswitch on every host.
   vswitches = set()
   for host in self.get_host_list():
      conf = host.config
      current_host_vswitches = set()
      for vswitch in conf.network.vswitch:
         current_host_vswitches.add(vswitch.name)
      if len(vswitches) == 0:
         vswitches = current_host_vswitches
      else:
         vswitches = vswitches.union(current_host_vswitches)

   return vswitches

def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """

   client = VsphereClient()
   client.connect()

   # network = client._get_obj_by_id([vim.Network], 'dvportgroup-1076')
   # network = client._get_obj_by_id([vim.dvs.DistributedVirtualPortgroup], 'dvportgroup-1076')
   network = client._get_obj_by_name([vim.Network], 'VM Network')
   print network
   #
   print type(network)

   print isinstance(network, vim.Network)
   # print network.parent.name
   # print network.parent.parent.name
   #print network.parent.parent.parent.name

   # vswitches = get_vswitches()



   # network_obj = client._get_obj_by_name([vim.Network], "192.168.84.0/24")
   # print dir(network_obj)
   # print network_obj.summary
   # print network_obj.effectiveRole

   # network_obj = client._get_obj_by_name([vim.dvs.DistributedVirtualPortgroup], 'dvPortGroup')
   # print dir(network_obj)
   # print network_obj.summary
   # print network_obj.effectiveRole

   # network_obj1 = client._get_obj_by_id([vim.Network], "network-1594")

   # print dir(network_obj)
   # print network_obj
   # print network_obj._moIdserver.guest.guestState

   datacenter = client._get_obj_by_id([vim.Datacenter],
                                    "datacenter-21")
   nicspec = vim.vm.device.VirtualDeviceSpec()
   # Info level as this is something that was requested in the
   # blueprint
   nicspec.operation = \
       vim.vm.device.VirtualDeviceSpec.Operation.add
   nicspec.device = vim.vm.device.VirtualVmxnet3()

   nicspec.device.wakeOnLanEnabled = True
   nicspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()

   nicspec.device.connectable.connected = True
   nicspec.device.connectable.startConnected = True
   nicspec.device.connectable.allowGuestControl = True

   #print dir(nicspec.device.connectable)

   #print nicspec.device.connectable.status


# Start program
if __name__ == "__main__":
   main()