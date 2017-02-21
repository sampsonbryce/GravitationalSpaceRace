from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from client.models import *


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
    text = message.content['text'].split(',')
    print('text', text)
    name = text[0]
    position = text[1]
    print(name, position)
    Group("{0}-client".format(l_map.lobby.id)).send({
        "name": name,
        "position": position,
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-client".format(l_map.lobby.id)).discard(message.reply_channel)


