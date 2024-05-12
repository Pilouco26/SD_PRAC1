import time
import grpc
from p1.BackEnd import xatPrivat_pb2_grpc, xatPrivat_pb2
import threading

class ChatClient:
    def __init__(self, server_ip, server_port, client_port, client_id, receiver_id):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_port = client_port
        self.client_id = client_id
        self.receiver_id = receiver_id
        self.nomChat = ""
        self.channel = grpc.insecure_channel(f'{server_ip}:{server_port}')
        self.stub = xatPrivat_pb2_grpc.ChatServiceStub(self.channel)
        self.listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        self.listen_thread.start()

    def send_message(self, message):
        print(f"Sending message: {message}")
        response = self.stub.SendMessage(
            xatPrivat_pb2.ChatMessage(from_id=self.client_id, to_id=self.receiver_id, message=message))
        print(f"Message sent. Response: {response}")

    def listen_for_messages(self):
        while True:
            try:
                print("Listening for messages")
                response = self.stub.ReceiveMessage(xatPrivat_pb2.ClientID(client_id=self.client_id))
                print("Message received")
                if response.message:  
                    print(f"Message received from {response.from_id}: {response.message}")
            except grpc.RpcError as e:
                print(f"Error receiving message: {e}")

def run_client(server_ip, server_port, client_port, client_id, receiver_id):
    client = ChatClient(server_ip, server_port, client_port, client_id, receiver_id)
    send_thread = threading.Thread(target=client.listen_for_messages, daemon=True)
    send_thread.start()


    while True:
        time.sleep(1)


if __name__ == '__main__':
    server_ip = input("Enter the server IP address: ")
    server_port = input("Enter the server port: ")
    client_port = input("Enter this client's port: ")
    client_id = input("Enter this client's ID: ")
    receiver_id = input("Enter the receiver's ID: ")

    run_client(server_ip, server_port, client_port, client_id, receiver_id)
