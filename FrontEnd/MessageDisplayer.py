class MessageDisplayer:
    def __init__(self, message_handler):
        self.message_handler = message_handler

    def display_messages(self):
        messages = self.message_handler.get_messages()
        for message in messages:
            print("Message:", message)


