# channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
#                 stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)
import threading

import grpc


def can_commit(self):
    # Conectarse al chat utilizando gRPC
    try:
        # Crear un canal gRPC hacia el servidor
        channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
        # stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)
        #
        # # Llamar al método Connect del servidor
        # response = stub.Connect(xatPrivat_pb2.ConnectionRequest(client_id=self.client.username,
        #                                                         client_address=f'{self.client.ip_address}:{self.client.port}'))
        response = 0
        # Mostrar mensaje de conexión exitosa
        if response.message == 'Connected':
            Thread = threading.Thread(target=self.receive_messages, daemon=True)
            Thread.start()
    except grpc.RpcError as e:
        print(f"Error connecting to chat: {e}")




def receive_messages(self):

    return


def have_committed(self):

    return
