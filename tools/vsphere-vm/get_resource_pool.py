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
   resource_pool = {'name': u'deployment', 'id': 'resgroup-440'}

   myresource_pool = client._get_obj_by_id([vim.ResourcePool], resource_pool['id'])
   print myresource_pool.name

   myresource_pool = client._get_obj_by_name([vim.ResourcePool], resource_pool['name'])
   print myresource_pool

# Start program
if __name__ == "__main__":
   main()