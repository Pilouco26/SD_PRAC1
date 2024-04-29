import time
import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc
import threading

class PrivateChatClient:
    def __init__(self, username):
        self.username = username
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = xatPrivat_pb2_grpc.PrivateChatStub(self.channel)
        self.connected = False

    def connect(self):
        # Conecta con el servidor
        response = self.stub.Connect(xatPrivat_pb2.ConnectRequest(username=self.username))
        if response.success:
            print(f"Conectado como {self.username}")
            self.connected = True
        else:
            print("Fallo en la conexión")

    def send_message(self, to, message):
        # Envía un mensaje a otro usuario
        response = self.stub.SendMessage(xatPrivat_pb2.Message(from_user=self.username, to=to, message=message))
        if response.success:
            print("Mensaje enviado con éxito")
        else:
            print("Fallo al enviar el mensaje")

    def receive_messages(self):
        # Recibe mensajes del servidor
        while self.connected:
            for message in self.stub.ReceiveMessages(xatPrivat_pb2.Empty(username=self.username)):
                print(f"Nuevo mensaje de {message.from_user}: {message.message}")
    
    def is_user_connected(self, username):
        # Verifica si el usuario está conectado
        response = self.stub.IsUserConnected(xatPrivat_pb2.ConnectRequest(username=username))
        return response.success
    
    def disconnect(self):
        # Desconecta del servidor
        response = self.stub.Disconnect(xatPrivat_pb2.ConnectRequest(username=self.username))
        if response.success:
            print(f"Desconectado como {self.username}")
            self.connected = False
        else:
            print("Fallo al desconectar")

def start_receiving_messages(client):
    threading.Thread(target=client.receive_messages).start()

client2 = PrivateChatClient('Miguel')
client2.connect()
start_receiving_messages(client2)
client2.send_message('Oriol', 'Hola')
client2.send_message('Oriol', 'Be i tu?')
client2.disconnect()