import amqp_client

fibonacci_rpc = amqp_client.create_client()
print '2'
response = fibonacci_rpc.call('2')
print 'waiting'
print response