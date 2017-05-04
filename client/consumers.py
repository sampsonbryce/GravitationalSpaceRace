from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from client.models import *
import json

# ----------------------CHAT--------------------------------
# Connected to websocket.connect
@channel_session_user_from_http
def ws_chat_connect(message):
    print('chat connect')
    l_map = LobbyUserMap.objects.get(user=message.user)
    message.reply_channel.send({"accept": True})
    Group("{0}-chat".format(l_map.lobby.id)).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_chat_receive(message):
    print('sending chat message')
    l_map = LobbyUserMap.objects.get(user=message.user)
    text = message.content['text']
    print('text', text)
    Group("{0}-chat".format(l_map.lobby.id)).send({
        "text": json.dumps({
            "username": message.user.username,
            "message": text
        })
    })
    # name = text[:text.index(',')]
    # position = text[text.index(',')+1:]
    # position_data = json.loads(str(position))
    # print(name, position_data)
    # Group("{0}-chat".format(l_map.lobby.id)).send({
    #     "text": json.dumps({
    #         "name": name,
    #         "position": position
    #     })
    # })


# Connected to websocket.disconnect
@channel_session_user
def ws_chat_disconnect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-chat".format(l_map.lobby.id)).discard(message.reply_channel)



# ----------------------CONTROL--------------------------------
@channel_session_user_from_http
def ws_control_connect(message):
    print('CONTROL connect')
    l_map = LobbyUserMap.objects.get(user=message.user)
    message.reply_channel.send({"accept": True})
    Group("{0}-control".format(l_map.lobby.id)).add(message.reply_channel)

@channel_session_user
def ws_control_receive(message):
    admin_controls = ["start"]
    user_controls = ["leave", "join"]

    print("CONTROL:", message)
    action = message.content['text']
    l_map = LobbyUserMap.objects.get(user=message.user)

    if action in admin_controls and not l_map.is_admin:
        print('NOT ADMIN')
        return

    if action in user_controls:
        action = "lobby_change"

    Group("{0}-control".format(l_map.lobby.id)).send({
        "text": json.dumps({
            "action": action,
        })
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_control_disconnect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-control".format(l_map.lobby.id)).discard(message.reply_channel)



# ----------------------GAME DATA--------------------------------
@channel_session_user_from_http
def ws_game_connect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    message.reply_channel.send({"accept": True})
    Group("{0}-game".format(l_map.lobby.id)).add(message.reply_channel)

@channel_session_user
def ws_game_receive(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    text = message.content['text']
    name = text[:text.index(',')]
    position = text[text.index(',')+1:]
    position_data = json.loads(str(position))
    print(name, position_data)
    Group("{0}-game".format(l_map.lobby.id)).send({
        "text": json.dumps({
            "name": name,
            "position": position
        })
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_game_disconnect(message):
    l_map = LobbyUserMap.objects.get(user=message.user)
    Group("{0}-game".format(l_map.lobby.id)).discard(message.reply_channel)


