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

    print task.info
    print task.info.result
    return task.info.result


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    client = VsphereClient()
    client.connect()

    server_names = ['good101']
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
    adaptermap.adapter.dnsDomain = inputs['domain']

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

    if adaptermap:
        customspec = vim.vm.customization.Specification()
        customspec.nicSettingMap = [adaptermap]

        if True:
            password = 'Passw0rd12--'

            # We use GMT without daylight savings if no timezone is
            # supplied, as this is as close to UTC as we can do
            timezone = 90

            ident = vim.vm.customization.Sysprep()
            ident.userData = vim.vm.customization.UserData()
            ident.guiUnattended = vim.vm.customization.GuiUnattended()
            ident.identification = vim.vm.customization.Identification()

            # Configure license data file required for window 2003 and 2000
            ident.licenseFilePrintData = vim.vm.customization.LicenseFilePrintData()
            ident.licenseFilePrintData.autoMode = vim.vm.customization.LicenseFilePrintData.AutoMode().perServer
            ident.licenseFilePrintData.autoUsers = 10

            # Configure userData
            ident.userData.computerName = vim.vm.customization.FixedName()
            ident.userData.computerName.name = inputs['vm_name']
            # Without these vars, customization is silently skipped
            # but deployment 'succeeds'
            ident.userData.fullName = inputs['vm_name']
            ident.userData.orgName = "Organisation"
            ident.userData.productId = ""

            # Configure guiUnattended
            ident.guiUnattended.autoLogon = False
            ident.guiUnattended.password = vim.vm.customization.Password()
            ident.guiUnattended.password.plainText = True
            ident.guiUnattended.password.value = password
            ident.guiUnattended.timeZone = timezone

            # Adding windows options
            options = vim.vm.customization.WinOptions()
            options.changeSID = True
            options.deleteAccounts = False
            customspec.options = options

        customspec.identity = ident
        globalip = vim.vm.customization.GlobalIPSettings()
        if inputs['dns']:
            globalip.dnsServerList = inputs['dns']
        customspec.globalIPSettings = globalip

    print customspec
    # For multipple NIC configuration contact me.
    print "Reconfiguring VM  . . ."

    task = server.Customize(spec=customspec)
    wait_for_task(task)


# Start program
if __name__ == "__main__":
    main()
