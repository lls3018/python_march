#!/usr/bin/env python
"""
Written by Reuben ur Rahman
Github: https://github.com/rreubenur
Email: reuben.13@gmail.com

Linked clone example
"""

import atexit
import requests.packages.urllib3 as urllib3
import ssl

from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect

from tools import cli
from tools import tasks
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')

    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                    help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                    help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=True, action='store',
                    help='Password to use when connecting to host')

    parser.add_argument('-v', '--vm_name',
                        required=True,
                        action='store',
                        help='Name of the new VM')

    parser.add_argument('--template_name',
                        required=True,
                        action='store',
                        help='Name of the template/VM you are cloning from')

    parser.add_argument('--datacenter_name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the Datacenter you wish to use.')

    parser.add_argument('--cluster_name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the cluster you wish to use')

    parser.add_argument('--host_name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the cluster you wish to use')

    args = parser.parse_args()

    return args


def get_obj(content, vimtype, name, folder=None):
    obj = None
    if not folder:
        folder = content.rootFolder
    container = content.viewManager.CreateContainerView(folder, vimtype, True)
    for item in container.view:
        if item.name == name:
            obj = item
            break
    return obj


def _clone_vm(si, template, vm_name, vm_folder, location):
    clone_spec = vim.vm.CloneSpec(
        powerOn=True, template=False, location=location,
        snapshot=template.snapshot.rootSnapshotList[0].snapshot)
    task = template.Clone(name=vm_name, folder=vm_folder, spec=clone_spec)
    tasks.wait_for_tasks(si, [task])
    print "Successfully cloned and created the VM '{}'".format(vm_name)


def _get_relocation_spec(host, resource_pool, datastore):
    relospec = vim.vm.RelocateSpec()
    relospec.diskMoveType = 'createNewChildDiskBacking'
    relospec.host = host
    relospec.pool = resource_pool
    relospec.datastore = datastore
    return relospec


def _take_template_snapshot(si, vm):
    if len(vm.rootSnapshot) < 1:
        task = vm.CreateSnapshot_Task(name='test_snapshot',
                                      memory=False,
                                      quiesce=False)
        tasks.wait_for_tasks(si, [task])
        print "Successfully taken snapshot of '{}'".format(vm.name)


def get_obj_list(content, vimtype):
    content = content
    container_view = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    objects = container_view.view
    container_view.Destroy()
    return objects

def main():
    args = get_args()

    urllib3.disable_warnings()
    si = None
    context = None

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=args.host,user=args.user,
                                            pwd=args.password,
                                            port=int(args.port),
                                            sslContext=context)

    atexit.register(Disconnect, si)
    print "Connected to vCenter Server"

    content = si.RetrieveContent()

    datacenter = get_obj(content, [vim.Datacenter], args.datacenter_name)
    if not datacenter:
        raise Exception("Couldn't find the Datacenter with the provided name "
                        "'{}'".format(args.datacenter_name))

    cluster = get_obj(content, [vim.ClusterComputeResource], args.cluster_name,
                      datacenter.hostFolder)

    if not cluster:
        raise Exception("Couldn't find the Cluster with the provided name "
                        "'{}'".format(args.cluster_name))

    resource_pool = get_obj(content, [vim.ResourcePool],"deployment")

    datastore = get_obj(content, [vim.Datastore],"Datastore")

    host_obj = None
    for host in cluster.host:
        if host.name == args.host_name:
            host_obj = host
            break

    vm_folder = datacenter.vmFolder

    template = get_obj(content, [vim.VirtualMachine], args.template_name,
                       vm_folder)

    if not template:
        raise Exception("Couldn't find the template with the provided name "
                        "'{}'".format(args.template_name))

    vmconf = vim.vm.ConfigSpec()
    print vmconf

    location = _get_relocation_spec(host_obj, resource_pool, datastore)
    #_take_template_snapshot(si, template)

    #tree = template.snapshot.rootSnapshotList
    #snapshot_id = "5"
    #snapshotList = []
    #find_snapshot(tree, snapshot_id,snapshotList)
    #print snapshotList[0].name ,snapshotList[0].snapshot

    #_clone_vm(si, template, args.vm_name, vm_folder, location)


def find_snapshot(snapshot_tree, snapshot_id, snapshotList):
    if len(snapshot_tree) == 0:
        return
    for snapshot in snapshot_tree:
        if (snapshot.id == int(snapshot_id)):
            snapshotList.append(snapshot)
        find_snapshot(snapshot.childSnapshotList, snapshot_id, snapshotList)


def get_snapshot2(tree,snapshotList):
    if len(tree) == 0:
        return
    for el in tree:
        snapshotList.append(el.snapshot)
        get_snapshot2(el.childSnapshotList,snapshotList)


def get_snapshot(tree):
    snapshotList = []
    for el in tree:
        snapshotList.append(el.name)
        if len(el.childSnapshotList) > 0:
            snapshotList.append(get_snapshot(el.childSnapshotList))
    return snapshotList




if __name__ == "__main__":
    main()

