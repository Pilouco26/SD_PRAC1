import grpc
from concurrent import futures
import xatPrivat_pb2
import xatPrivat_pb2_grpc
import queue

class PrivateChatServicer(xatPrivat_pb2_grpc.PrivateChatServicer):
    def __init__(self):
        self.clients = {}  # Almacena los clientes conectados
        self.messages = {}  # Almacena los mensajes para cada cliente

    def Connect(self, request, context):
        # Almacena el nombre de usuario y la cola de mensajes del cliente en los diccionarios
        self.clients[request.username] = context
        self.messages[request.username] = queue.Queue()
        return xatPrivat_pb2.ConnectResponse(success=True)

    def SendMessage(self, request, context):
        # Añade el mensaje a la cola de mensajes del destinatario si está conectado
        if request.to in self.clients:
            self.messages[request.to].put(xatPrivat_pb2.Message(from_user=request.from_user, message=request.message))
            return xatPrivat_pb2.MessageAck(success=True)
        else:
            return xatPrivat_pb2.MessageAck(success=False)

    def ReceiveMessages(self, request, context):
        # Produce mensajes a medida que se reciben
        while True:
            if not self.messages[request.username].empty():
                yield self.messages[request.username].get()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_PrivateChatServicer_to_server(PrivateChatServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
