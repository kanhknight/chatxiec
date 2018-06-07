from flask import Flask, render_template, request
from flask_socketio import *
app = Flask(__name__)
app.config['SECRET_KEY'] = '123@#@45690@#'
socketio = SocketIO(app)

#Tin nhắn global 
@socketio.on('Client-send-message', namespace= '/message')
def Client_send_message(data):
    print('User {0} gửi tin nhắn!'.format(request.sid))

    # Server gửi tin nhắn global cho tất cả các user
    emit('Server-send-message', data, namespace='/message', broadcast = True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host= '127.0.0.1', port= 3000, debug = True)