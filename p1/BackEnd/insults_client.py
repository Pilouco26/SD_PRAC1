import pika

def callback(ch, method, properties, body):
    print("Insulto recibido:", body.decode())

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='insults')

channel.basic_consume(queue='insults',
                      on_message_callback=callback,
                      auto_ack=True)

print('Esperando insultos...')
channel.start_consuming()
