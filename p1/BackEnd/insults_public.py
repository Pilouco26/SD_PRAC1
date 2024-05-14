import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='insults')

insults = input("Ingresa los insultos separados por coma: ").split(',')

for insult in insults:
    channel.basic_publish(exchange='',
                          routing_key='insults',
                          body=insult.strip())

    print("Insulto enviado:", insult.strip())

connection.close()


