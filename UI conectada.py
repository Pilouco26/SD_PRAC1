import threading
import tkinter as tk
from tkinter import simpledialog
import socket
import grpc

import xatPrivat_pb2
import xatPrivat_pb2_grpc


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
            "Send message": self.send_message
        }

        for option in self.options:
            button = tk.Button(self, text=option, command=self.options[option])
            button.pack()

        self.display_chat_active = False  # Flag to indicate if chat display is active

    def display_chat(self):
        if not self.display_chat_active:
            # Abrir una ventana de chat dedicada
            chat_window = ChatWindow(self.client)
            chat_window.mainloop()
            self.display_chat_active = True
        else:
            # Implementar lógica para ocultar la ventana de chat
            pass

    def connect_to_chat(self):
        chat_id = simpledialog.askstring("Connect to Chat", "Enter chat ID:")
        if chat_id:
            # Conectarse al chat utilizando gRPC
            try:
                self.client.nomChat = chat_id
                # Crear un canal gRPC hacia el servidor
                channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
                stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)

                # Llamar al método Connect del servidor
                response = stub.Connect(xatPrivat_pb2.ConnectionRequest(client_id=self.client.username,
                                                                        client_address=f'{self.client.ip_address}:{self.client.port}'))

                # Mostrar mensaje de conexión exitosa
                if response.message == 'Connected':
                    Thread = threading.Thread(target=self.receive_messages, daemon=True)
                    Thread.start()
            except grpc.RpcError as e:
                print(f"Error connecting to chat: {e}")

    #FALLA AIXO
    def receive_messages(self):
        # Implementar recepción de mensajes utilizando gRPC
        try:
            # Crear un canal gRPC hacia el servidor
            channel = grpc.insecure_channel(f'{self.client.server_ip}:{self.client.server_port}')
            stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)

            # Llamar al método ReceiveMessage del servidor
            message = stub.ReceiveMessage(xatPrivat_pb2.ClientID(client_id=self.client.username))
            print(message)

        except grpc.RpcError as e:
            print(f"Error receiving message: {e}")

    def send_message(self):
        message = simpledialog.askstring("Send message", "Enter chat ID:")
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


class ChatWindow(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.title("Chat Window")
        self.geometry("400x300")

        self.message_list = tk.Listbox(self)
        self.message_list.pack(expand=True, fill="both")

        self.entry = tk.Entry(self)
        self.entry.pack(expand=True, fill="x")
        self.entry.bind("<Return>", self.send_message)


def get_local_ip_and_port():
    # Fetch the local IP address of the machine
    ip_address = socket.gethostbyname(socket.gethostname())
    print(ip_address)
    # Find an available port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return ip_address, port


class Client:
    def __init__(self, username, server_ip, server_port, ip_address, port):
        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port
        self.ip_address = ip_address
        self.port = port
        self.nomChat = ""


def main():
    # Obtener detalles del cliente
    username = simpledialog.askstring("Username", "Enter your username:")
    if not username:
        return

    # Obtener detalles del servidor
    server_ip = "localhost"
    server_port = "50051"

    # Obtener detalles del cliente local
    ip_address, port = get_local_ip_and_port()

    # Crear instancia del cliente
    client = Client(username, server_ip, server_port, ip_address, port)
    print(client, ip_address)
    # Crear instancia de la interfaz de usuario y ejecutar la aplicación
    iu = ChatUI(client)
    iu.mainloop()


if __name__ == "__main__":
    main()
