from __main__ import socketio

from flask_socketio import *
from models.collection import *
from flask import session

@socketio.on('client-send-play-pause', namespace='/player')
def play_pause(data):
    emit('server-send-play-pause', data, broadcast=True)
    print(data)

@socketio.on('connect', namespace='/message')
def test_connect():
    a = 20
    emit('my response', {'data': 'Connected'})
    emit('server_sent_count', a, namespace = "/message", broadcast = True)

@socketio.on('disconnect', namespace = '/message')
def test_disconnect():
    a = 10000
    print('Disconnected')
    emit('server_sent_count', a, namespace = "/message", broadcast = True)
    
@socketio.on('client-sent-message', namespace = "/message")
def client_sent_message(data):
    username = session['loggedin']
    # Luu message vao csdl
    user = User.objects(username = username).first()
    new_message = Message(
        userid = str(user.id),
        clientid = data['userid'],
        message = data['message'],
        datetime = data['date']
    )
    new_message.save()

# Lay message trong csdll
    message_send_user = Message.objects().with_id(new_message.id)
    data_to_send = {
        'clientid' : message_send_user.clientid,
        'username': username,
        'message' : message_send_user.message
    }

    emit('server_sent_message', data_to_send, namespace = "/message", broadcast = True)

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
