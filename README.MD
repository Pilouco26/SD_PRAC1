Projecte final



To run:

1. start docker app
2. write this line on terminal:
3. docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
4. start client
5. start server

Bugs known:

If you close a client, chat_discovery will crash, so needing all clients up. 