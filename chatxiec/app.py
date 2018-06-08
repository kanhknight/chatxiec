from flask import Flask, render_template, request
from flask_socketio import *
from jinja2 import *
app = Flask(__name__)
app.config['SECRET_KEY'] = '123@#@45690@#'
socketio = SocketIO(app)

#Tin nhắn global 
@socketio.on('Client-send-message', namespace= '/message')
def Client_send_message(data):
    print('User {0} gửi tin nhắn!'.format(request.sid))

    # Server gửi tin nhắn global cho tất cả các user
    emit('Server-send-message-all-client', data, namespace='/message', broadcast = True)


# Xử lý gửi tin nhắn private cho 1 user được chỉ định
# Bước 1: Xử lý đăng ký user vào Dictionary
users = {}
@socketio.on('private-message-send-username', namespace = '/private-mesage')
def receive_username(username):
    users[username] = request.sid
    print(users)

# Bước 2: Xử lý gửi tin nhắn tới user được chỉ định
@socketio.on('private-message-from-client', namespace = '/private-mesage')
def receive_private_message(tinnhan):
    receipient_session_id = users[tinnhan['username']]
    message = tinnhan['message']
    print(message)
    
    emit('private-message-from-server-receipient', message, room = receipient_session_id)
    emit('private-message-from-server-sender', message, room = request.sid)

# Kết thúc xử lý tin nhắn private cho user được chỉ định

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host= '127.0.0.1', port= 3000, debug = False)