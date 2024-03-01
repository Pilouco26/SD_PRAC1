import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://localhost:9000')

print(proxy.add_insult('Moc'))
print(proxy.get_insults())
print(proxy.insult_me())
