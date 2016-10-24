import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl

class VsphereClient(object):

    def __init__(self):
        self.host = '192.168.84.9'
        self.user = 'root'
        self.pwd = 'vmware'
        self.port = 443

    def connect(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
            ssl._create_default_https_context = ssl._create_unverified_context
            self.si = SmartConnect(host=self.host,
                                   user=self.user,
                                   pwd=self.pwd,
                                   port=self.port)
            atexit.register(Disconnect, self.si)
            self._get_content()
            return self
        except vim.fault.InvalidLogin:
            raise Exception(
                "Could not login to vSphere on {host} with provided "
                "credentials".format(host=self.host)
            )

    def _get_content(self):
        if "content" not in locals():
            self.content = self.si.RetrieveContent()
        return self.content

    def get_obj_list(self, vimtype):
        content = self._get_content()
        container_view = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        objects = container_view.view
        container_view.Destroy()
        return objects

    def _has_parent_name_or_id(self, obj, parent, recursive, by_name=True):
        if parent is None:
            return True
        if by_name:
            if obj.parent is not None:
                if obj.parent.name == parent:
                    return True
                elif recursive:
                    return self._has_parent_name_or_id(obj.parent, parent, recursive, by_name=True)
            # If we didn't confirm that the object has a parent by now, it doesn't
            return False
        else:
            if obj.parent is not None:
                if obj.parent._moId == parent:
                    return True
                elif recursive:
                    return self._has_parent_name_or_id(obj.parent, parent, recursive, by_name=False)
            # If we didn't confirm that the object has a parent by now, it doesn't
            return False

    def _get_obj_by_name(self, vimtype, name, parent=None,
                         recursive_parent=False, by_parent_name=True):
        obj = None
        objects = self.get_obj_list(vimtype)
        for c in objects:
            if c.name == name:
                if self._has_parent_name_or_id(c, parent, recursive_parent, by_parent_name):
                    obj = c
                    break
        return obj

    def _get_obj_by_id(self, vimtype, id, parent=None,
                       recursive_parent=False, by_parent_name=True):
        obj = None
        objects = self.get_obj_list(vimtype)
        for c in objects:
            if c._moId == id:
                if self._has_parent_name_or_id(c, parent, recursive_parent, by_parent_name):
                    obj = c
                    break
        return obj

    def get_vm_networks(self, vm):
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
        for dev in vm.config.hardware.device:
            if hasattr(dev, 'macAddress'):
                nics.append(dev)

        networks = []
        for nic in nics:
            distributed = hasattr(nic.backing, 'port') and isinstance(
                nic.backing.port,
                vim.dvs.PortConnection,
            )

            network_name = None
            if distributed:
                mapping_id = nic.backing.port.portgroupKey
                for network in vm.network:
                    if hasattr(network, 'key'):
                        if mapping_id == network.key:
                            network_name = network.name
            else:
                # If not distributed, the port group name can be retrieved
                # directly
                network_name = nic.backing.deviceName

            if network_name is None:
                raise Exception(
                    'Could not get network name for device with MAC address '
                    '{mac} on VM {vm}'.format(mac=nic.macAddress, vm=vm.name)
                )

            networks.append({
                'name': network_name,
                'distributed': distributed,
                'mac': nic.macAddress,
            })

        return networks