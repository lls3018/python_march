import pika
import time
import broker_config


def callback(ch, method, properties, body):
    print(ch, method, properties)
    print(" [x] Received %r" % body)
    time.sleep(15)
    ch.basic_ack(delivery_tag=method.delivery_tag)

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

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.queue_declare(queue='hello1')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='hello1')
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()