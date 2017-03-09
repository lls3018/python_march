import amqp_client

fibonacci_rpc = amqp_client.create_client(amqp_id='a1')
dic1 = {'instance_id': '1', 'node_id': 'Server', 'deployment_id': 'cdea123445'}
print dic1
print 'waiting...'
response = fibonacci_rpc.call(dic1)


print response
print type(response)