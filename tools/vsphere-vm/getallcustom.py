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

    customization_spec_name = 'wenqi-good'
    customization_spec_name = 'wenqi-good-win2'
    # print client.content.customizationSpecManager.DoesCustomizationSpecExist(name=customization_spec_name)
    customspec = client.content.customizationSpecManager.GetCustomizationSpec(name=customization_spec_name)
    print customspec
    print type(customspec)

    # print dir(client.content.customizationSpecManager)


    # print client.content.customizationSpecManager.info


# Start program
if __name__ == "__main__":
    main()
