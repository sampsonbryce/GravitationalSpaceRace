from channels.routing import route, include
from client.routing import client_routing

channel_routing = [
    include(client_routing, path=r"^/client"),
    route("websocket.receive", 'core.consumers.ws_message'),
    route("websocket.connect", 'core.consumers.ws_add'),
    route("websocket.disconnet", 'core.consumers.ws_disconnect'),
]
