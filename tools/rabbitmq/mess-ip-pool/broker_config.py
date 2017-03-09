
import ssl

config = {}

# Provided as variables for retrieval by amqp_client and logger as required
# broker_ssl_enabled = config.get('broker_ssl_enabled', False)
# broker_cert_path = config.get('broker_cert_path', '')
# broker_username = config.get('broker_username', 'cloudchef')
# broker_password = config.get('broker_password', 'c10udch3f')
# broker_hostname = config.get('broker_hostname', '192.168.84.28')
# broker_port = 5672


broker_ssl_enabled = config.get('broker_ssl_enabled', False)
broker_cert_path = config.get('broker_cert_path', '')
broker_username = config.get('broker_username', 'guest')
broker_password = config.get('broker_password', 'guest')
broker_hostname = config.get('broker_hostname', 'localhost')
broker_port = 5672



print config