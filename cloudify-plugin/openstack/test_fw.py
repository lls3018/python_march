
import openstack_plugin_common as common

SERVER_STATUS_VERIFY_RESIZE = 'VERIFY_RESIZE'

class OpenstackClients():

    def clients_custom_configuration(self):
        # tests for clients custom configuration, passed via properties/inputs

        inputs_cfg = {
            'username': 'admin',
            'password': 'crowbar',
            'auth_url': 'http://192.168.126.2:5000/v2.0',
            'region': 'RegionOne',
            'tenant_name': 'admin'
        }


        nova_client, neut_client, cind_client = \
            self._create_clients(inputs_cfg)
        return nova_client, neut_client, cind_client

    def _create_clients(self, inputs_cfg):

        orig_nova_client = common.NovaClientWithSugar
        orig_neut_client = common.NeutronClientWithSugar
        orig_cind_client = common.CinderClientWithSugar
        #orig_keys_client = common.keystone_client.Client

        try:
            common.NovaClient().get(config=inputs_cfg)
            common.NeutronClient().get(config=inputs_cfg)
            common.CinderClient().get(config=inputs_cfg)
            #common.KeystoneClient().get(config=inputs_cfg)
        except:
            print "except"
        finally:
            common.NovaClientWithSugar = orig_nova_client
            common.NeutronClientWithSugar = orig_neut_client
            common.CinderClientWithSugar = orig_cind_client
            #common.keystone_client.Client = orig_keys_client

            return (common.NovaClient().get(config=inputs_cfg), common.NeutronClient().get(config=inputs_cfg), common.CinderClient().get(config=inputs_cfg) )


def _wait_firewall_to_targetstatus(neutron_client, firewall_id, targetstatus, timeout=120, sleep_interval=5):
    import time
    timeout = time.time() + timeout
    while time.time() < timeout:
        firewall_status = describe_firewall_status_from_id(neutron_client, firewall_id)
        print('Waiting for firewall "{}" to be {}. current status: {}'
                        .format(firewall_id, targetstatus, firewall_status))
        if firewall_status == targetstatus:
            return
        time.sleep(sleep_interval)
    return


def describe_firewall_status_from_id(neutron_client, firewall_id):
    firewall = neutron_client.show_firewall(firewall_id)['firewall']
    return firewall.get('status')


if __name__ == '__main__':
    client = OpenstackClients()
    nova_client, neut_client, cind_client = client.clients_custom_configuration()
    #print neut_client.list_firewalls()
    # print neut_client.list_firewall_policies()
    # print neut_client.list_firewall_rules()

    print '-------'

    # firewall_rule_req = {
    #     'name': '',
    #     "action": "allow",
    #     "protocol": None,
    #     'shared': False,
    #     'enabled': True
    #     }
    #
    # firewall_rule_obj = neut_client.create_firewall_rule({'firewall_rule': firewall_rule_req})['firewall_rule']
    # print firewall_rule_obj
    #
    # firewall_policy_req = {
    #         "name": "test-policy",
    #         "firewall_rules": [
    #             firewall_rule_obj['id']
    #         ]
    #     }
    #
    # firewall_policy_obj = neut_client.create_firewall_policy({'firewall_policy': firewall_policy_req})['firewall_policy']
    # print firewall_policy_obj
    #
    #
    # firewall_req = {
    #     "router_ids": [],
    #     "admin_state_up": True,
    #     "firewall_policy_id": '1ef7a919-9db1-4db8-83be-5b7225e9bfe4'
    # }
    #
    # firewall_obj = neut_client.create_firewall({'firewall': firewall_req})['firewall']
    # print firewall_obj


    # firewall_obj = neut_client.show_firewall('5762bf86-6def-48c3-b442-2db7941cc66d')['firewall']
    #
    # firewall_rules = neut_client.show_firewall_policy(firewall_obj['firewall_policy_id'])['firewall_policy']
    #
    #
    #
    # firewall_id = '5762bf86-6def-48c3-b442-2db7941cc66d'
    #
    # firewall_req = {
    #     "router_ids": ['165f06b9-b3b6-41ea-a5b0-d2e36bdaa660'],
    # }
    #
    # firewall_obj = neut_client.update_firewall(firewall_id, {'firewall': firewall_req})['firewall']
    # print firewall_obj
    #
    # _wait_firewall_ready(neut_client, firewall_id)
    #
    # firewall_req = {
    #     "router_ids": ['0f0ff546-0998-433d-b67a-4b99e316dfa5'],
    # }
    #
    # firewall_obj = neut_client.update_firewall(firewall_id, {'firewall': firewall_req})['firewall']
    # print firewall_obj


    firewall_id = '55c1f784-8884-420a-8609-9b9340b21ecc'
    firewall_req = {"router_ids": []}
    neut_client.update_firewall(firewall_id, {'firewall': firewall_req})
    _wait_firewall_to_targetstatus(neut_client, firewall_id, 'INACTIVE')

    firewall_obj = neut_client.show_firewall(firewall_id)['firewall']
    firewall_policy_obj = neut_client.show_firewall_policy(firewall_obj['firewall_policy_id'])['firewall_policy']
    firewall_rules = firewall_policy_obj.get('firewall_rules')

    print firewall_rules

    firewall_policy_req = {"firewall_rules": []}
    print neut_client.update_firewall_policy(firewall_policy_obj['id'], {'firewall_policy': firewall_policy_req})

    print neut_client.show_firewall(firewall_id)['firewall']

    for firewall_rule in firewall_rules:
         neut_client.delete_firewall_rule(firewall_rule)

    neut_client.delete_firewall(firewall_id)
    neut_client.delete_firewall_policy(firewall_policy_obj['id'])

