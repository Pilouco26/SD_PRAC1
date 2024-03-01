import grpc
from concurrent import futures
import time

# import the generated classes
import insultingServer_pb2
import insultingServer_pb2_grpc

# import the original insultingServer.py
from insulting_service import insulting_service


# create a class to define the server functions, derived from
# insultingServer_pb2_grpc.InsultingServiceServicer
class InsultingServiceServicer(insultingServer_pb2_grpc.InsultingServiceServicer):

    def AddInsult(self, insult, context):
        insulting_service.add_insult(insult.value)
        response = insultingServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def GetInsults(self, empty, context):
        insults = insulting_service.get_insults()
        response = insultingServer_pb2.Insults()
        response.value.extend(insults)
        return response

    def InsultMe(self, empty, context):
        insult = insulting_service.insult_me()
        response = insultingServer_pb2.Insult()
        response.value = insult
        return response

    def get_shout_insults(self, empty, context):

        return 0


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
insultingServer_pb2_grpc.add_InsultingServiceServicer_to_server(
    InsultingServiceServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
