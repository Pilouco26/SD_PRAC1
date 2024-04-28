import threading

import pika
import redis


class Client:

    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.message_queue_key = 'petitions'
        self.pubsub_channel_prefix = 'petition_channel:'
        ##ERROR AQUI AMB LA CONEXIO(docker)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.message_callback = None
        global nomChat
        nomChat = "chat1"
        self.channel.exchange_declare(exchange=nomChat, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)

        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=nomChat, queue=self.queue_name, routing_key='chatID')

        self.messages = []  # Store received messages here

        def callback(ch, method, properties, body):
            # Process the message and store it in self.messages
            self.messages.append(body.decode())  # Assuming messages are bytes, decode them
            print(f"{body.decode()}")  # Print the message for reference

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)

    def connect_to_chat(self, chat_id):
        print("This is the chat id:" + chat_id)
        chat_id = str(chat_id)
        global nomChat
        nomChat = chat_id
        data = "connection:" + nomChat
        self.redis.lpush(self.message_queue_key, data)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        # Attempt to bind the queue with the chat ID as routing key
        self.channel.exchange_declare(exchange=nomChat, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)

        self.queue_name = result.method.queue
        result = self.channel.queue_bind(exchange=nomChat, queue=self.queue_name, routing_key='chatID')

        # Check if binding was successful (result.response code should be 0)
        if result.method.NAME == 'Queue.BindOk':
            print(f"Successfully bound to chat ID: {chat_id}")
            self.start_message_handler()
        else:
            print(f"Failed to bind to chat ID: {chat_id}. Error code: {result.response}")

    def register(self, petition_data):
        if isinstance(petition_data, Client):
            data = petition_data.username + ':' + petition_data.ip_address + ':' + str(petition_data.port) + ":r"
            self.redis.lpush(self.message_queue_key, data)
            print("Petition sent successfully.")
        else:
            print("Error: petition_data should be an instance of the Client class.")

    # PROVA FUNCIONALITATS
    # PROVAR 2 CLIENTS EN EL MATEIX XAT

    def set_message_callback(self, callback):
        self.message_callback = callback

    def callback(self, ch, method, properties, body):
        message = body.decode()
        self.messages.append(message)  # Save the message
        if self.message_callback:
            self.message_callback(message)

    # error callback
    def start_message_handler(self):
        while True:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()


class MessageHandler:
    def __init__(self, username, ip_address, port):
        self.chat_consumer = Client(username, ip_address, port)
        self.chat_consumer.set_message_callback(self.handle_message)

    def handle_message(self, message):
        print(message)
        # Add your message handling logic here

    def get_messages(self):
        return self.chat_consumer.messages


class MessageDisplayer:
    def __init__(self, message_handler):
        self.message_handler = message_handler

    def display_messages(self):
        messages = self.message_handler.get_messages()
        for message in messages:
            print("Message:", message)
