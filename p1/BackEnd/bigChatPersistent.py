import pika



class ChatConsumerPersistent:
    def __init__(self, exchange):
        self.message_callback = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        ###MIRAR QUE FA UNIC UN CHAT
        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key='chatID')
        self.messages = []

    ##PROVAR
    def set_message_callback(self, callback):
        self.message_callback = callback

    def callback(self, ch, method, properties, body):
        message = body.decode()
        self.messages.append(message)  # Save the message
        print(message+"i received messaged")

    def start_message_handler(self):
        while True:
            self.start_consuming()

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()
