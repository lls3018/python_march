
import amqp_client

fibonacci_rpc = amqp_client.create_client(amqp_id='a3')
response = fibonacci_rpc.call('3')
print 'waiting'
print response