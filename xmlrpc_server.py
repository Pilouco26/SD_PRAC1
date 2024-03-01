from xmlrpc.server import SimpleXMLRPCServer
import logging
from insulting_service import insulting_service

logging.basicConfig(level=logging.INFO)

server = SimpleXMLRPCServer(
    ('0.0.0.0', 9000),
    logRequests=True
)

server.register_instance(insulting_service)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
