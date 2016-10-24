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
   ident = vim.vm.customization.Sysprep()
   ident.licenseFilePrintData = vim.vm.customization.LicenseFilePrintData()
   ident.licenseFilePrintData.autoMode = vim.CustomizationLicenseDataMode('perServer')
   ident.licenseFilePrintData.autoMode = vim.vm.customization.LicenseFilePrintData.AutoMode().perSeat
   ident.licenseFilePrintData.autoUsers = 10


   print ident.licenseFilePrintData

   print type(vim.CustomizationLicenseDataMode())
   print type(vim.vm.customization.LicenseFilePrintData.AutoMode())
   #print type(vim.CustomizationLicenseDataMode('perSeat'))

# Start program
if __name__ == "__main__":
   main()