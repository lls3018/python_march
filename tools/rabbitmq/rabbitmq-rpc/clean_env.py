import pika
import broker_config

if __name__ == '__main__':

    credentials = pika.credentials.PlainCredentials(
        username=broker_config.broker_username,
        password=broker_config.broker_password)
    connection_parameters = pika.ConnectionParameters(
        host=broker_config.broker_hostname,
        port=broker_config.broker_port,
        credentials=credentials,
        ssl=False,
        ssl_options={})

    queue = 'wenqi_ip_pool_result'

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.queue_delete(queue=queue)