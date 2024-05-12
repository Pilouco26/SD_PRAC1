import threading
from tkinter import simpledialog

import pika
import redis
import ast


class Client:

    def __init__(self, username, ip_address, port, server_ip, server_port):
        self.init = False
        self.queue_name = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.username = username
        self.ip_address = ip_address
        self.server_ip = server_ip
        self.server_port = server_port
        self.port = port
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.message_queue_key = 'petitions'
        self.message_queue_display_key = 'display'
        self.pubsub_channel_prefix = 'petition_channel:'
        self.pubsub_channel_display_prefix = 'display_channel:'
        self.nomChat = "init"
        self.conf(self.nomChat)
        self.message_callback = None
        self.messages = {}  # Store received messages here

    def connect_to_chat(self, chat_id):
        chat_id = str(chat_id)
        self.nomChat = chat_id
        data = "connection:" + self.nomChat
        self.redis.lpush(self.message_queue_key, data)
        thread = threading.Thread(target=self.configuration_chat, args=(chat_id,))
        thread.daemon = True
        thread.start()

    def connect_to_chat2(self, chat_id):
        self.nomChat = chat_id

    # Sets channel
    def conf(self, chat_id):
        self.nomChat = chat_id
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.nomChat, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        result = self.channel.queue_bind(exchange=self.nomChat, queue=self.queue_name, routing_key='chatID')
        self.init = True
        return result

    def chat_discovery(self):
        self.nomChat = "chat_discovery"
        data = "connection:" + self.nomChat
        self.redis.lpush(self.message_queue_key, data)
        thread = threading.Thread(target=self.configuration_chat, args=(self.nomChat,))
        thread.daemon = True
        thread.start()

    # Checks and calls Handler
    def configuration_chat(self, chat_id):
        result = self.conf(chat_id)
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

    def set_message_callback(self, callback):
        self.message_callback = callback

    def callback(self, ch, method, properties, body):
        message = body.decode()
        if method.exchange not in self.messages:
            self.messages[method.exchange] = []
        self.messages[method.exchange].append(message)  # Save the message with exchange name as the key
        if method.exchange == self.nomChat:
            if method.exchange != "chat_discovery":
                print(message)
            else:
                # Check if message is a string representation of a list
                if message.startswith('[') and message.endswith(']'):
                    message_list = ast.literal_eval(message)
                    print("These are the chats discovered:")
                    for chat in message_list[1:]:  # Skip the first chat
                        print(chat)
    def start_message_handler(self):
        while True:
            self.start_consuming()

    def start_consuming(self):
        if self.channel.is_open and self.init is True:
            self._consume_in_thread()

    def _consume_in_thread(self):
        try:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            print(f"Error in thread: {e}")

    def stop_consuming(self):
        self.channel.stop_consuming()
