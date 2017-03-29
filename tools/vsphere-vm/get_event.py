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
import time


def _wait_customization_success(client, vm):
    # Step1 : Create a EventFilterSpecByEntity
    efespec = vim.event.EventFilterSpec.ByEntity()
    efespec.entity = vm
    efespec.recursion = vim.event.EventFilterSpec.RecursionOption.all
    # Step2 :Event Spec Filter
    efspec = vim.event.EventFilterSpec()
    efspec.entity = efespec

    events = client.content.eventManager.QueryEvents(efspec)
    for event in events:
        print type(event)

    # while True:
    #     events = client.content.eventManager.QueryEvents(efspec)
    #     if not events:
    #         continue
    #     print("Waiting for CustomizationSucceeded")
    #     print (events[-1]).fullFormattedMessage
    #     for event in events:
    #         if type(event) is vim.event.CustomizationSucceeded:
    #             print("CustomizationSucceeded")
    #             break
    #     else:
    #         time.sleep(15)
    #         continue
    #     break


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    client = VsphereClient()
    client.connect()

    server_names = ['Server-kanwj3']
    for server_name in server_names:
        server = client._get_obj_by_name([vim.VirtualMachine], server_name)
        print server.name, server._moId
        print dir(server)

    system_ready = server.guest.guestOperationsReady
    system_state = server.guest.guestState
    system_uptime = server.summary.quickStats.uptimeSeconds

    #print server.guest.net
    print system_ready
    print system_state
    print system_uptime

    _wait_customization_success(client, server)

# Start program
if __name__ == "__main__":
    main()
