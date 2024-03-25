import socket
import sys
import tkinter as tk
from tkinter import simpledialog

import redis


class Client:
    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.message_queue_key = 'petitions'
        self.message_queue_key = 'petitions'
        self.pubsub_channel_prefix = 'petition_channel:'

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
            "Connect chat": self.connect_to_chat,
            "Subscribe to group chat": self.subscribe_to_group_chat,
            "Discover chats": self.discover_chats,
            "Access insult channel": self.access_insult_channel,
            "test nameserver": self.get_ip_nameserver
        }

        for option in self.options:
            button = tk.Button(self, text=option, command=self.options[option])
            button.pack()

    def connect_to_chat(self):
        chat_id = simpledialog.askstring("Connect to Chat", "Enter chat ID:")
        if chat_id:
            self.client.connect_to_chat(chat_id)

    def get_ip_nameserver(self):
        chat_id = simpledialog.askstring("get ip", "Enter chat ID:")
        if chat_id:
            if chat_id:
                #send petition
                data = chat_id + ':' + self.client.ip_address + ':' + str(self.client.port)
                self.client.redis.lpush(self.client.message_queue_key, data)
                print("Petition sent successfully.")

                #retrieve ip
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


def main():
    username = simpledialog.askstring("Username", "Enter your username:")
    if not username:
        sys.exit()

    ip_address, port = get_local_ip_and_port()
    client = Client(username, ip_address, port)
    client.register(client)
    iu = ChatUI(client)
    iu.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()
