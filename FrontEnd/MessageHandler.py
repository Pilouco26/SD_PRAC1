from FrontEnd.Client import Client


class MessageHandler:
    def __init__(self, username, ip_address, port):
        self.chat_consumer = Client(username, ip_address, port)
        self.chat_consumer.set_message_callback(self.handle_message)

    def handle_message(self, message):
        print(message)
        # Add your message handling logic here

    def get_messages(self):
        return self.chat_consumer.messages