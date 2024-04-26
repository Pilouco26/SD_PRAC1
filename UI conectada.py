import asyncio
import socket
import sys
import tkinter as tk
from tkinter import simpledialog

import pika
import redis

from bigChat import ChatConsumer, MessageHandler


class Client:
    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.message_queue_key = 'petitions'
        self.message_queue_key = 'petitions'
        self.pubsub_channel_prefix = 'petition_channel:'
        self.chatConsumer = ChatConsumer()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='chat_exchange', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.channel.queue_bind(exchange='chat_exchange', queue=self.queue_name, routing_key='chatID')
        self.queue_name = result.method.queue

        self.messages = []  # Store received messages here

        def callback(ch, method, properties, body):
            # Process the message and store it in self.messages
            self.messages.append(body.decode())  # Assuming messages are bytes, decode them
            print(f"{body.decode()}")  # Print the message for reference

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)

    def connect_to_chat(self, chat_id):
        print("This is the chat id:"+chat_id)
        chat_id = str(chat_id)
        # Attempt to bind the queue with the chat ID as routing key
        result = self.channel.queue_bind(exchange='chat_exchange', queue=self.queue_name, routing_key='hola')

        # Check if binding was successful (result.response code should be 0)
        if result.method.NAME == 'Queue.BindOk':
            print(f"Successfully bound to chat ID: {chat_id}")
            self.channel.start_consuming()
        else:
            print(f"Failed to bind to chat ID: {chat_id}. Error code: {result.response}")

    def register(self, petition_data):
        if isinstance(petition_data, Client):
            data = petition_data.username + ':' + petition_data.ip_address + ':' + str(petition_data.port) + ":r"
            self.redis.lpush(self.message_queue_key, data)
            print("Petition sent successfully.")
        else:
            print("Error: petition_data should be an instance of the Client class.")


class ChatUI(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.title("Client UI")
        self.geometry("400x300")

        self.label = tk.Label(self, text="Welcome, " + self.client.username)
        self.label.pack(pady=10)

        self.options = {
            "Connect chat": self.connectChatDisplayer,
            "Subscribe to group chat": self.subscribe_to_group_chat,
            "Discover chats": self.discover_chats,
            "Access insult channel": self.access_insult_channel,
            "Test nameserver": self.get_ip_nameserver,
            "Test group": self.send_message_group,
            "Display Chat": self.display_chat
        }

        for option in self.options:
            button = tk.Button(self, text=option, command=self.options[option])
            button.pack()

        self.display_chat_active = False  # Flag to indicate if chat display is active

    def display_chat(self):
        if not self.display_chat_active:
            self.client.start_display_chat()
            self.display_chat_active = True
        else:
            self.client.stop_display_chat()
            self.display_chat_active = False

    def connectChatDisplayer(self):
        chat_id = simpledialog.askstring("Connect to Chat", "Enter chat ID:")
        print(chat_id)
        if chat_id:
            self.client.connect_to_chat(chat_id)

    def get_ip_nameserver(self):
        chat_id = simpledialog.askstring("get ip", "Enter chat ID:")
        if chat_id:
            if chat_id:
                # send petition
                data = chat_id + ':' + self.client.ip_address + ':' + str(self.client.port)
                self.client.redis.lpush(self.client.message_queue_key, data)
                print("Petition sent successfully.")

                # retrieve ip
                channel = self.client.pubsub_channel_prefix + self.client.ip_address
                pubsub = self.client.redis.pubsub()
                pubsub.subscribe([channel])
                for message in pubsub.listen():
                    if message['type'] == 'message':
                        # Change this line
                        ip_address, port = message['data'].decode('utf-8').split(':')
                        # Process the received IP address and port, e.g., connect to it
                        print("Received IP:", ip_address, "Port:", port)
                        # You can now establish a connection using this IP address and port
                        break  # Stop listening after receiving the first message

    def send_message_group(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        message = simpledialog.askstring("Send Message", "message here bitch")
        message = "@" + self.client.username + " : " + message
        if message:
            # Declare the exchange
            channel.exchange_declare(exchange='chat_exchange', exchange_type='direct')
            # Publish the message to the exchange with the routing key 'chatID'
            channel.basic_publish(exchange='chat_exchange', routing_key='chatID', body=message)

    def subscribe_to_group_chat(self):
        group_chat_id = simpledialog.askstring("Subscribe to Group Chat", "Enter group chat ID:")
        if group_chat_id:
            self.client.subscribe_to_group_chat(group_chat_id)

    def discover_chats(self):
        self.client.discover_chats()

    def access_insult_channel(self):
        insult_message = simpledialog.askstring("Insult Channel", "Enter insult message:")
        if insult_message:
            receiver_username = simpledialog.askstring("Insult Channel", "Enter receiver's username:")
            if receiver_username:
                self.client.send_insult(insult_message, receiver_username)


def get_local_ip_and_port():
    # Fetch the local IP address of the machine
    ip_address = socket.gethostbyname(socket.gethostname())
    # Find an available port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return ip_address, port


import threading


def start_message_handler():
    message_handler2 = MessageHandler()
    asyncio.run(message_handler2.chat_consumer.start_consuming())


def main():
    username = simpledialog.askstring("Username", "Enter your username:")
    if not username:
        sys.exit()

    ip_address, port = get_local_ip_and_port()
    client = Client(username, ip_address, port)
    client.register(client)
    iu = ChatUI(client)

    # Start a new thread to execute start_message_handler while the Tkinter window is open
    thread = threading.Thread(target=start_message_handler)
    thread.daemon = True  # Make the thread a daemon thread so it terminates when the main thread (Tkinter) exits
    thread.start()

    iu.mainloop()


if __name__ == "__main__":
    main()

