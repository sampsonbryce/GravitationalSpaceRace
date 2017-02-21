from channels.routing import route

client_routing = [
    route("websocket.receive", 'client.consumers.ws_message'),
    route("websocket.connect", 'client.consumers.ws_add'),
    route("websocket.disconnet", 'client.consumers.ws_disconnect'),
]