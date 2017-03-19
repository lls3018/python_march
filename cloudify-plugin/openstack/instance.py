from novaclient import exceptions as nova_exceptions


def _normalize_nics(nics):
    def _normalize(nic):
        if 'port-id' in nic and 'net-id' in nic:
            nic = nic.copy()
            del nic['net-id']
        return nic
    return [_normalize(nic) for nic in nics]


def _merge_nics(management_network_id, *nics_sources):
    """Merge nics_sources into a single nics list, insert mgmt network if needed.

    nics_sources are lists of networks received from several sources
    (server properties, relationships to networks, relationships to ports).
    Merge them into a single list, and if the management network isn't present
    there, prepend it as the first network.
    """
    merged = []
    for nics in nics_sources:
        merged.extend(nics)
    if management_network_id is not None and \
            not any(nic['net-id'] == management_network_id for nic in merged):
        merged.insert(0, {'net-id': management_network_id})
    return merged


def create_vm(nova_client, neutron_client, **kwargs):
    """
    Creates a server. Exposes the parameters mentioned in
    http://docs.openstack.org/developer/python-novaclient/api/novaclient.v1_1
    .servers.html#novaclient.v1_1.servers.ServerManager.create
    """

    management_network_name = 'fixed'

    server = {
        'name': 'Server_test1',
        'image': 'eb50e469-4401-4bcf-afb6-e661e89db275',
        'flavor': 2
    }

    if 'meta' not in server:
        server['meta'] = dict()

    management_network = neutron_client.cosmo_get_named('network', management_network_name)
    management_network_id = management_network['id']
    if management_network_id is None:
        raise Exception(
            "Nova server with NICs requires "
            "'management_network_name' in properties or id "
            "from provider context, which was not supplied")

    nics = _merge_nics(
        management_network_id,
        server.get('nics', []))
    nics = _normalize_nics(nics)
    server['nics'] = nics
    server['meta']['cloudify_management_network_id'] = management_network_id
    server['meta']['cloudify_management_network_name'] = management_network_name

    print("Creating VM with parameters: {0}".format(str(server)))
    print(
        "Asking Nova to create server. All possible parameters are: {0})"
        .format(','.join(server.keys())))

    try:
        s = nova_client.servers.create(**server)
    except nova_exceptions.BadRequest as e:
        print str(e)
        raise Exception

    return s.id
