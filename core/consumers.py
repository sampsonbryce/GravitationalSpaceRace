from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from client.models import *

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    print('Being added to channel')
    l_map = LobbyUserMap.objects.get(user=message.user)
    message.reply_channel.send({"accept": True})
    Group("{0}-chat".format(l_map.lobby.id)).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    print('sent message to socket', message)
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-chat".format(l_map.lobby.id)).send({
        "text": "[{0}] {1}".format(message.user.username, message.content['text']),
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-chat".format(l_map.lobby.id)).discard(message.reply_channel)


