from channels.routing import route, include
from client.routing import client_routing

channel_routing = [
    include(client_routing, path=r"^/client"),
]
