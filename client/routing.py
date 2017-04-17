from channels.routing import route, include

lobby_chat_routing = [
    route("websocket.receive", 'client.consumers.ws_chat_receive', path=r'^$'),
    route("websocket.connect", 'client.consumers.ws_chat_connect', path=r'^$'),
    route("websocket.disconnet", 'client.consumers.ws_chat_disconnect', path=r'^$'),
]

lobby_control_routing = [
    route("websocket.receive", 'client.consumers.ws_control_receive', path=r'^$'),
    route("websocket.connect", 'client.consumers.ws_control_connect', path=r'^$'),
    route("websocket.disconnect", 'client.consumers.ws_control_disconnect', path=r'^$'),
]

lobby_game_routing = [
    route("websocket.receive", 'client.consumers.ws_game_receive', path=r'^$'),
    route("websocket.connect", 'client.consumers.ws_game_connect', path=r'^$'),
    route("websocket.disconnect", 'client.consumers.ws_game_disconnect', path=r'^$'),
]


client_routing = [
    include(lobby_chat_routing, path=r'^/lobby/chat/$'),
    include(lobby_control_routing, path=r'^/lobby/control/$'),
    include(lobby_game_routing, path=r'^/lobby/game/$')
]