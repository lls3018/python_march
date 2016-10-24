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

inputs = {'vcenter_ip': '10.10.10.211',
          'vcenter_password': 'Password123',
          'vcenter_user': 'Administrator',
          'vm_name': 'reuben-test',
          'isDHCP': False,
          'vm_ip': '10.10.10.212',
          'subnet': '255.255.255.0',
          'gateway': '10.10.10.1',
          'dns': ['11.110.135.51', '11.110.135.52'],
          'domain': 'asiapacific.mycomp.net'
          }


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

    server_names = ['good100']
    for server_name in server_names:
        server = client._get_obj_by_name([vim.VirtualMachine], server_name)
        print server.name, server._moId
        # get_vm_networks(server)

    if server.runtime.powerState != 'poweredOff':
        print "WARNING:: Power off your VM before reconfigure"
        import sys
        sys.exit()

    adaptermap = vim.vm.customization.AdapterMapping()
    globalip = vim.vm.customization.GlobalIPSettings()
    adaptermap.adapter = vim.vm.customization.IPSettings()

    isDHDCP = inputs['isDHCP']
    if not isDHDCP:
        """Static IP Configuration"""
        adaptermap.adapter.ip = vim.vm.customization.FixedIp()
        adaptermap.adapter.ip.ipAddress = inputs['vm_ip']
        adaptermap.adapter.subnetMask = inputs['subnet']
        adaptermap.adapter.gateway = inputs['gateway']
        globalip.dnsServerList = inputs['dns']

    else:
        """DHCP Configuration"""
        adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()

    adaptermap.adapter.dnsDomain = inputs['domain']

    globalip = vim.vm.customization.GlobalIPSettings()

    # For Linux . For windows follow sysprep
    ident = vim.vm.customization.LinuxPrep(domain=inputs['domain'],
                                           hostName=vim.vm.customization.FixedName(name=inputs['vm_name']))

    customspec = vim.vm.customization.Specification()
    # For only one adapter
    customspec.identity = ident
    customspec.nicSettingMap = [adaptermap]
    customspec.globalIPSettings = globalip

    # Configuring network for a single NIC
    # For multipple NIC configuration contact me.

    print "Reconfiguring VM Networks . . ."

    task = server.Customize(spec=customspec)
    wait_for_task(task)


# Start program
if __name__ == "__main__":
    main()
