import socket
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

import pika

from p1.FrontEnd.Client import Client


class ChatUI(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.title("Client UI")
        self.geometry("400x300")
        self.nomChat = "discovery_chat"
        self.chats = []
        self.chatsSubscribed = ['chat_discovery']
        self.chatsTransients = ['chat_discovery']
        self.label = tk.Label(self, text="Welcome, " + self.client.username)
        self.label.pack(pady=10)
        self.client.connect_to_chat("chat_discovery")
        self.options = {
            "Connect to chat": self.chat_connector,
            "Subscribe to chat": self.chatSubscriber,
            "Write in group connected": self.send_message_group,
            "Discover chats": self.discover_chats,
            "Access insult channel": self.access_insult_channel,
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

    def chatSubscriber(self):
        chat_id = simpledialog.askstring("Connect to Chat", "Enter chat ID:")

        if chat_id:
            mode = messagebox.askquestion("Mode", "Transient", icon='question', type='yesno')
            mode = 'transient' if mode == 'yes' else 'persistent'
            self.client.connect_to_chat(chat_id)
            self.chatsSubscribed.append(chat_id)
            if mode == 'transient':
                self.chatsTransients.append(chat_id)
            print(f"Connected to chat {chat_id} in {mode} mode")
        else:
            print("Invalid chat ID")

    def chat_connector(self):
        chat_id = simpledialog.askstring("Connect to Chat", "Enter chat ID:")
        if chat_id and chat_id in self.chatsSubscribed:
            if chat_id == self.nomChat:
                print("Already connected")
            else:
                print("Connected to Chat", chat_id)
                self.nomChat = chat_id
                self.client.connect_to_chat2(chat_id)
                messages = self.client.messages
                if chat_id in messages and chat_id not in self.chatsTransients:
                    for message in messages[chat_id]:  # Iterate over the list of messages
                        print(message)  # Print each message on a new line

        else:
            print("No chat found, we need you to be subscribed to", chat_id)

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

    # RABBIT MQ
    def get_chats(self):
        self.client.chat_discovery()

    def send_message_group(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        message = simpledialog.askstring("Send Message", "message here bitch")
        message = "@" + self.client.username + " : " + message
        if message:
            # Declare the exchange
            channel.exchange_declare(exchange=self.nomChat, exchange_type='direct')
            # Publish the message to the exchange with the routing key 'chatID'
            channel.basic_publish(exchange=self.nomChat, routing_key='chatID', body=message)

    def discover_chats(self):
        self.nomChat = "chat_discovery"
        self.get_chats()
        self.client.redis.lpush(self.client.message_queue_key, "chat_discovery")
        print("Petition sent successfully.")

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


def main():
    username = simpledialog.askstring("Username", "Enter your username:")
    if not username:
        sys.exit()

    ip_address, port = get_local_ip_and_port()
    client = Client(username, ip_address, port)
    client.register(client)
    iu = ChatUI(client)
    iu.mainloop()


if __name__ == "__main__":
    main()
