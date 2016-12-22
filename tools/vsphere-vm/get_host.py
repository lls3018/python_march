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


def get_host_state(host):
    host_state = (host.runtime.connectionState == 'connected') \
                 and (host.runtime.powerState == 'poweredOn') \
                 and (host.runtime.inMaintenanceMode is False)
    return host_state


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    client = VsphereClient()
    client.connect()

    host_list = client.get_obj_list([vim.HostSystem])
    for host in host_list:
        if host.name == '192.168.84.85':
            print host.name
            print host.runtime.inMaintenanceMode
            #print host.runtime
            #print host.runtime
            print get_host_state(host)


    # datastore2 = client._get_obj_by_name([vim.Datastore], 'datastore1')
    #
    # #print "datastore:", datastore2, datastore2.name
    # for host in datastore2.host:
    #     print get_host_state(host.key)



# Start program
if __name__ == "__main__":
    main()
