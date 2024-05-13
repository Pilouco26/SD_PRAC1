# channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
#                 stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)
import threading

import grpc

import xatPrivat_pb2
import xatPrivat_pb2_grpc


class Slave:

    def __init__(self, node_id, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server_ip = "localhost"
        self.server_port = "32770"
        self.node_id = node_id
        self.nodes = []

    def connect_to_chat_grpc(self):
        try:
            channel = grpc.insecure_channel(f'{self.server_ip}:{self.server_port}')
            stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)

            # Llamar al método Connect del servidor
            response = stub.Connect(xatPrivat_pb2.ConnectionRequest(client_id=self.node_id,
                                                                    client_address=f'{self.ip_address}:{self.client.port}'))

            # Mostrar mensaje de conexión exitosa
            if response.message == 'Connected':
                Thread = threading.Thread(target=self.receive_messages, daemon=True)
                Thread.start()
        except grpc.RpcError as e:
            print(f"Error connecting to chat: {e}")



    def receive_messages(self):
        # Implementar recepción de mensajes utilizando gRPC
        try:
            # Crear un canal gRPC hacia el servidor
            channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
            stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)

            # Llamar al método ReceiveMessage del servidor
            for node in self.nodes:
                message = stub.ReceiveMessage(xatPrivat_pb2.ClientID(client_id=self.node))
                if message.message == 'canCommit?':
                    return "this"


        except grpc.RpcError as e:
            print(f"Error receiving message: {e}")

    def send_message(self):
        if message:
            # Implementar envío de mensaje utilizando gRPC
            try:
                # Crear un canal gRPC hacia el servidor
                channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
                stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)

                # Llamar al método SendMessage del servidor
                response = stub.SendMessage(
                    xatPrivat_pb2.ChatMessage(from_id=self.client.username, to_id=self.client.nomChat, message=message))

                # Mostrar mensaje de confirmación
                print(f"Message sent. Response: {response}")
            except grpc.RpcError as e:
                print(f"Error sending message: {e}")

    def have_committed(self):
        return
