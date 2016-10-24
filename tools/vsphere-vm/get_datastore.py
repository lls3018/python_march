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

from pyVmomi import vim
from ServerClient import VsphereClient

def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """
   client = VsphereClient()
   client.connect()
   datastore = {'name': u'datastore1', 'id': 'datastore-1572'}

   datastore1 = client._get_obj_by_id([vim.Datastore], datastore['id'])
   print "datastore1", datastore1


   #print datastore1, datastore1.name

   datastore2 = client._get_obj_by_name([vim.Datastore], datastore['name'])

   print "datastore2", datastore2, datastore2.name
   relospec = vim.vm.RelocateSpec()
   relospec.datastore = datastore1

   clonespec = vim.vm.CloneSpec()
   clonespec.location = relospec

   #print clonespec


   print datastore1, datastore2
   print  '------'
   selected_datastore = datastore1 if datastore1 else datastore2
   print selected_datastore.name

   datastore1 = client._get_obj_by_id([vim.Datastore],
                                    "datastore-1572")
   print datastore1.name

   datastore2 = client._get_obj_by_id([vim.Datastore],
                                       "datastore-453")
   print datastore2.name

  # print datastore1.name, datastore2._moId

   datastore = {'name': None, 'id': None}
   datastore1 = client._get_obj_by_id([vim.Datastore], None)
   print datastore1

   datastore2 = client._get_obj_by_name([vim.Datastore], datastore['name'])
   print datastore2

   #folder = None
   #destfolder = folder if folder else datacenter.vmFolder
   #print destfolder

   #print dir(datacenter)
   #print "----vmFolder1---"
   #print datacenter.vmFolder
   #print "----vmFolder2---"
   #print dir(datacenter.vmFolder)
   #print datacenter.vmFolder.childEntity

   #'vim.Folder:group-v28',
   #'vim.Folder:group-v813',
   #'vim.Folder:group-v7941',

   #print datacenter._moId

   #server = client._get_obj_by_id([vim.VirtualMachine], 'vm-1514')
   #print server.guest.net
   #print '-------------'
   #for network in server.guest.net:
   #   network_name = network.network
   #   network_id = client._get_obj_by_name([vim.Network], network_name)._moId
   #   print network_name, network_id



# Start program
if __name__ == "__main__":
   main()