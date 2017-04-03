from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.generic.websockets import JsonWebsocketConsumer
from client.models import *
import json

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    message.reply_channel.send({"accept": True})
    Group("{0}-client".format(l_map.lobby.id)).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    text = message.content['text']
    name = text[:text.index(',')]
    position = text[text.index(',')+1:]
    position_data = json.loads(str(position))
    print(name, position_data)
    Group("{0}-client".format(l_map.lobby.id)).send({
        "text": json.dumps({
            "name": name,
            "position": position
        })
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-client".format(l_map.lobby.id)).discard(message.reply_channel)


