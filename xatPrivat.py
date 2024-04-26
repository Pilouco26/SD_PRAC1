# chat_client.py

import grpc
import chat_pb2
import chat_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel("localhost:5001")

# create a stub (client)
stub = chat_pb2_grpc.ChatStub(channel)

# create a valid request message
user = input("Enter username: ")
message = chat_pb2.Message(user=user, content="Hello, world!")

# make the call
response = stub.SendMessage(message)

# et voila
print(response)
