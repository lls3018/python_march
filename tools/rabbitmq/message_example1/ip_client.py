import pika
import broker_config
import uuid

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

    corr_id = str(uuid.uuid4())

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.queue_declare(queue='hello1')

    channel.basic_publish(exchange='',
                          routing_key='hello1',
                          properties=pika.BasicProperties(
                              reply_to='hello1',
                              correlation_id=corr_id,
                          ),
                          body='Hello World-zeng')

    # channel.basic_publish(exchange='',
    #                       routing_key='hello',
    #                       body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()