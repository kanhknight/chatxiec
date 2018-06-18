from flask_socketio import emit, join_room
from models.collection import *
from flask import session

@socketio.on('joinroom', namespace = '/chatroom')
def on_join(data):
    username = session['loggedin']
    room = data
    join_room(room)
    emit('server_send_noti_to_user_join_room', data, namespace = "/chatroom", room = room)
    print(username + " Joined "+ room)

@socketio.on('client_sent_message_to_room', namespace ='/chatroom')
def client_sent_message_to_room(data):
    username = session['loggedin']
    user = User.objects(username = username).first()
    roomid = data['roomid']
    new_room_message = RoomMessage(
        roomid = roomid,
        userid = str(user.id),
        clientid = data['userid'],
        message = data['message'],
        datetime = data['date']
    )
    new_room_message.save()

    message_send = RoomMessage.objects().with_id(new_room_message.id)
    data_to_send_from_server = {
        'clientid' : message_send.clientid,
        'username': username,
        'message' : message_send.message
    }

    emit('server_sent_message_to_room', data_to_send_from_server, room = roomid)