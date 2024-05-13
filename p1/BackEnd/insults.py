import pika

class InsultChannel:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='insult_queue')

    def callback(self, ch, method, properties, body):
        insult = body.decode()
        print("Received insult:", insult)

    def start_insult_handler(self):
        self.channel.basic_consume(queue='insult_queue', on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for insults. To exit press CTRL+C')
        self.channel.start_consuming()

    def publish_insult(self, insult):
        self.channel.basic_publish(exchange='', routing_key='insult_queue', body=insult)
        print("Sent insult:", insult)
