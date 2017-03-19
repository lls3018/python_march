import json
import os

import neutronclient.v2_0.client as neutron_client
import neutronclient.common.exceptions as neutron_exceptions
import novaclient.v2.client as nova_client


class Config(object):

    OPENSTACK_CONFIG_PATH_ENV_VAR = 'OPENSTACK_CONFIG_PATH'
    OPENSTACK_CONFIG_PATH_DEFAULT_PATH = '~/openstack_config.json'

    def get(self):
        static_config = self._build_config_from_env_variables()
        env_name = self.OPENSTACK_CONFIG_PATH_ENV_VAR
        default_location_tpl = self.OPENSTACK_CONFIG_PATH_DEFAULT_PATH
        default_location = os.path.expanduser(default_location_tpl)
        config_path = os.getenv(env_name, default_location)
        try:
            with open(config_path) as f:
                Config.update_config(static_config, json.loads(f.read()))
        except IOError:
            pass
        return static_config

    @staticmethod
    def _build_config_from_env_variables():
        cfg = dict()

        def take_env_var_if_exists(cfg_key, env_var):
            if env_var in os.environ:
                cfg[cfg_key] = os.environ[env_var]

        take_env_var_if_exists('username', 'OS_USERNAME')
        take_env_var_if_exists('password', 'OS_PASSWORD')
        take_env_var_if_exists('tenant_name', 'OS_TENANT_NAME')
        take_env_var_if_exists('auth_url', 'OS_AUTH_URL')
        take_env_var_if_exists('region', 'OS_REGION_NAME')
        take_env_var_if_exists('neutron_url', 'OS_URL')
        take_env_var_if_exists('nova_url', 'NOVACLIENT_BYPASS_URL')

        return cfg

    @staticmethod
    def update_config(overridden_cfg, overriding_cfg):
        """ this method is like dict.update() only that it doesn't override
        with (or set new) empty values (e.g. empty string) """
        for k, v in overriding_cfg.iteritems():
            if v:
                overridden_cfg[k] = v


class OpenStackClient(object):

    REQUIRED_CONFIG_PARAMS = \
        ['username', 'password', 'tenant_name', 'auth_url']

    def get(self, config=None, *args, **kw):
        cfg = Config().get()
        if config:
            Config.update_config(cfg, config)

        self._validate_config(cfg)
        ret = self.connect(cfg, *args, **kw)
        ret.format = 'json'
        return ret

    def _validate_config(self, cfg):
        missing_config_params = self._get_missing_config_params(cfg)
        if missing_config_params:
            raise Exception(missing_config_params)

    def _get_missing_config_params(self, cfg):
        missing_config_params = \
            [param for param in self.REQUIRED_CONFIG_PARAMS if param not in
             cfg or not cfg[param]]
        return missing_config_params


class NovaClient(OpenStackClient):

    def connect(self, cfg):
        client_kwargs = dict(
            username=cfg['username'],
            api_key=cfg['password'],
            project_id=cfg['tenant_name'],
            auth_url=cfg['auth_url'],
            region_name=cfg.get('region', ''),
            http_log_debug=False
        )

        if cfg.get('nova_url'):
            client_kwargs['bypass_url'] = cfg['nova_url']

        client_kwargs.update(
            cfg.get('custom_configuration', {}).get('nova_client', {}))

        return NovaClientWithSugar(**client_kwargs)


class NeutronClient(OpenStackClient):

    def connect(self, cfg):
        client_kwargs = dict(
            username=cfg['username'],
            password=cfg['password'],
            tenant_name=cfg['tenant_name'],
            auth_url=cfg['auth_url'],
        )

        if cfg.get('neutron_url'):
            client_kwargs['endpoint_url'] = cfg['neutron_url']
        else:
            client_kwargs['region_name'] = cfg.get('region', '')

        client_kwargs.update(
            cfg.get('custom_configuration', {}).get('neutron_client', {}))

        return NeutronClientWithSugar(**client_kwargs)

_non_recoverable_error_codes = [400, 401, 403, 404, 409]


class ClientWithSugar(object):

    def cosmo_plural(self, obj_type_single):
        return obj_type_single + 's'

    def cosmo_get_named(self, obj_type_single, name, **kw):
        return self.cosmo_get(obj_type_single, name=name, **kw)

    def cosmo_get(self, obj_type_single, **kw):
        return self._cosmo_get(obj_type_single, False, **kw)

    def cosmo_get_if_exists(self, obj_type_single, **kw):
        return self._cosmo_get(obj_type_single, True, **kw)

    def _cosmo_get(self, obj_type_single, if_exists, **kw):
        ls = list(self.cosmo_list(obj_type_single, **kw))
        check = len(ls) > 1 if if_exists else len(ls) != 1
        if check:
            raise Exception(
                "Expected {0} one object of type {1} "
                "with match {2} but there are {3}".format(
                    'at most' if if_exists else 'exactly',
                    obj_type_single, kw, len(ls)))
        return ls[0] if ls else None


class NovaClientWithSugar(nova_client.Client, ClientWithSugar):

    def cosmo_list(self, obj_type_single, **kw):
        """ Sugar for xxx.findall() - not using xxx.list() because findall
        can receive filtering parameters, and it's common for all types"""
        obj_type_plural = self._get_nova_field_name_for_type(obj_type_single)
        for obj in getattr(self, obj_type_plural).findall(**kw):
            yield obj

    def cosmo_delete_resource(self, obj_type_single, obj_id):
        obj_type_plural = self._get_nova_field_name_for_type(obj_type_single)
        getattr(self, obj_type_plural).delete(obj_id)

    def get_id_from_resource(self, resource):
        return resource.id

    def get_name_from_resource(self, resource):
        return resource.name

    def get_quota(self, obj_type_single):
        raise RuntimeError(
            'Retrieving quotas from Nova service is currently unsupported '
            'due to a bug in Nova python client')

        self.client.authenticate()
        tenant_id = self.client.service_catalog.get_tenant_id()
        quotas = self.quotas.get(tenant_id)
        return getattr(quotas, self.cosmo_plural(obj_type_single))

    def _get_nova_field_name_for_type(self, obj_type_single):
        if obj_type_single == 'floatingip':
            # since we use the same 'openstack type' property value for both
            # neutron and nova floating-ips, this adjustment must be made
            # for nova client, as fields names differ between the two clients
            obj_type_single = 'floating_ip'
        return self.cosmo_plural(obj_type_single)


class NeutronClientWithSugar(neutron_client.Client, ClientWithSugar):

    def cosmo_list(self, obj_type_single, **kw):
        """ Sugar for list_XXXs()['XXXs'] """
        obj_type_plural = self.cosmo_plural(obj_type_single)
        for obj in getattr(self, 'list_' + obj_type_plural)(**kw)[
                obj_type_plural]:
            yield obj

    def cosmo_delete_resource(self, obj_type_single, obj_id):
        getattr(self, 'delete_' + obj_type_single)(obj_id)

    def get_id_from_resource(self, resource):
        return resource['id']

    def get_name_from_resource(self, resource):
        return resource['name']

    def get_quota(self, obj_type_single):
        tenant_id = self.get_quotas_tenant()['tenant']['tenant_id']
        quotas = self.show_quota(tenant_id)['quota']
        return quotas[obj_type_single]

    def cosmo_list_prefixed(self, obj_type_single, name_prefix):
        for obj in self.cosmo_list(obj_type_single):
            if obj['name'].startswith(name_prefix):
                yield obj

    def cosmo_delete_prefixed(self, name_prefix):
        # Cleanup all neutron.list_XXX() objects with names starting
        #  with self.name_prefix
        for obj_type_single in 'port', 'router', 'network', 'subnet',\
                               'security_group':
            for obj in self.cosmo_list_prefixed(obj_type_single, name_prefix):
                if obj_type_single == 'router':
                    ports = self.cosmo_list('port', device_id=obj['id'])
                    for port in ports:
                        try:
                            self.remove_interface_router(
                                port['device_id'],
                                {'port_id': port['id']})
                        except neutron_exceptions.NeutronClientException:
                            pass
                getattr(self, 'delete_' + obj_type_single)(obj['id'])

    def cosmo_find_external_net(self):
        """ For tests of floating IP """
        nets = self.list_networks()['networks']
        ls = [net for net in nets if net.get('router:external')]
        if len(ls) != 1:
            raise Exception(
                "Expected exactly one external network but found {0}".format(
                    len(ls)))
        return ls[0]
