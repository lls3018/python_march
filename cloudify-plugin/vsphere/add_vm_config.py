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

    server_names = ['windows-2']
    for server_name in server_names:
        server = client._get_obj_by_name([vim.VirtualMachine], server_name)
        print server.name, server._moId

    client = VsphereClient()
    client.connect()

    server_names = ['ubuntu-wenqi']
    for server_name in server_names:
        server = client._get_obj_by_name([vim.VirtualMachine], server_name)

    spec = vim.vm.ConfigSpec()
    opt = vim.option.OptionValue()
    spec.extraConfig = []

    options_values = {
        "custom_key5": "Ive tested very large xml and json, and base64 values here"
                       " and they work",
        "custom_key6": "Ive tested very large xml and json, and base64 values here"
                       " and they work",
        "custom_key7": "Ive tested very large xml and json, and base64 values here"
                       " and they work",
        "custom_key8": "update"
    }

    for k, v in options_values.iteritems():
        opt.key = k
        opt.value = v
        spec.extraConfig.append(opt)
        opt = vim.option.OptionValue()

    task = server.ReconfigVM_Task(spec)
    wait_for_task(task)
    print("Done setting values.")
    print("time to get them")
    keys_and_vals = server.config.extraConfig
    for opts in keys_and_vals:
        print("key: {0} => {1}".format(opts.key, opts.value))
    print("done.")


# Start program
if __name__ == "__main__":
    main()
