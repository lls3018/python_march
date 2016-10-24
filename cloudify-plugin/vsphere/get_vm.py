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
import time

from ServerClient import VsphereClient


def get_vm_networks(vm):
    """
        Get details of every network interface on a VM.
        A list of dicts with the following network interface information
        will be returned:
        {
            'name': Name of the network,
            'distributed': True if the network is distributed, otherwise
                           False,
            'mac': The MAC address as provided by vsphere,
        }
    """
    nics = []
    print('Getting NIC list')
    for dev in vm.config.hardware.device:
        if hasattr(dev, 'macAddress'):
            nics.append(dev)

    print('Got NICs: {nics}'.format(nics=nics))
    networks = []
    for nic in nics:
        print('Checking details for NIC {nic}'.format(nic=nic))
        distributed = hasattr(nic.backing, 'port') and isinstance(
            nic.backing.port,
            vim.dvs.PortConnection,
        )

        network_name = None
        if distributed:
            mapping_id = nic.backing.port.portgroupKey
            print(
                'Found NIC was on distributed port group with port group '
                'key {key}'.format(key=mapping_id)
            )
            for network in vm.network:
                if hasattr(network, 'key'):
                    print(
                        'Checking for match on network with key: '
                        '{key}'.format(key=network.key)
                    )
                    if mapping_id == network.key:
                        network_name = network.name
                        print(
                            'Found NIC was distributed and was on '
                            'network {network}'.format(
                                network=network_name,
                            )
                        )
        else:
            # If not distributed, the port group name can be retrieved
            # directly
            network_name = nic.backing.deviceName
            print(
                'Found NIC was on port group {network}'.format(
                    network=network_name,
                )
            )

        if network_name is None:
            print(
                'Could not get network name for device with MAC address '
                '{mac} on VM {vm}'.format(mac=nic.macAddress, vm=vm.name)
            )

        networks.append({
            'name': network_name,
            'distributed': distributed,
            'mac': nic.macAddress,
        })

    return networks


def get_ip_from_vsphere_nic_ips(nic):
    for ip in nic.ipAddress:
        if ip.startswith('169.254.') or ip.lower().startswith('fe80::'):
            # This is a locally assigned IPv4 or IPv6 address and thus we
            # will assume it is not routable
            print('Found locally assigned IP {ip}. '
                  'Skipping.'.format(ip=ip))
            continue
        else:
            return ip
    # No valid IP was found
    return None


def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
            print out
        else:
            out = '%s completed successfully.' % actionName
            print out
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        raise task.info.error
        print out

    return task.info.result


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    client = VsphereClient()
    client.connect()

    server_names = ['good']
    for server_name in server_names:
        server = client._get_obj_by_name([vim.VirtualMachine], server_name)
        print server.name, server._moId

    # Step1 : Create a EventFilterSpecByEntity
    efespec = vim.event.EventFilterSpec.ByEntity()
    efespec.entity = server
    efespec.recursion = vim.event.EventFilterSpec.RecursionOption.all
    # Step2 :Event Spec Filter
    efspec = vim.event.EventFilterSpec()
    efspec.entity = efespec
    # Step3: QueryEvents
    events = client.content.eventManager.QueryEvents(efspec)
    #print events
    for event in events:
        if type(event) is vim.event.CustomizationSucceeded:
            print event


    # print '-------'
    # vapp2 = client._get_obj_by_name([vim.ResourcePool], 'testApp')
    # print vapp2.name, vapp2
    # print type(vapp2)
    # print isinstance(vapp2, vim.VirtualApp)
    # for vm in vapp2.vm:
    #     print vm.name
    #
    # print "=========="
    # print '######'
    # vapp3 = client._get_obj_by_name([vim.ResourcePool], 'testApp')
    # print vapp3.name, vapp3
    # print type(vapp3)
    # print isinstance(vapp3, vim.ResourcePool)
    # for vm in vapp3.vm:
    #     print vm.name


# Start program
if __name__ == "__main__":
    main()
