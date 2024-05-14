import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='insults')

insults = ["Tonto", "Lleig", "Ruc", "Pocavergonya", "Desgraciat"]
for insult in insults:
    channel.basic_publish(exchange='',
                          routing_key='insults',
                          body=insult)
    print("Insulto enviado:", insult)

connection.close()

