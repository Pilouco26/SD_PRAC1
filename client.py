import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc

class PrivateChatClient:
    def __init__(self, username):
        self.username = username
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = xatPrivat_pb2_grpc.PrivateChatStub(self.channel)

    def connect(self):
        # Conecta con el servidor
        response = self.stub.Connect(xatPrivat_pb2.ConnectRequest(username=self.username))
        if response.success:
            print(f"Conectado como {self.username}")
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
        for message in self.stub.ReceiveMessages(xatPrivat_pb2.Empty(username=self.username)):
            print(f"Nuevo mensaje de {message.from_user}: {message.message}")

client1 = PrivateChatClient('Alice')
client1.connect()
client2 = PrivateChatClient('Bob')
client2.connect()
client1.send_message('Bob', 'Hola Bob')
client2.receive_messages()
client2.send_message('Alice', 'Hola')
client1.receive_messages()