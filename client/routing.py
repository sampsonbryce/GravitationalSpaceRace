from channels.routing import route

client_routing = [
    route("websocket.receive", 'client.consumers.ws_message', path=r'^/lobby_chat/$'),
    route("websocket.connect", 'client.consumers.ws_add', path=r'^/lobby_chat/$'),
    route("websocket.disconnet", 'client.consumers.ws_disconnect', path=r'^/lobby_chat/$'),
]