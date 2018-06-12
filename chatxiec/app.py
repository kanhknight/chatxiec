from flask import *
from flask_socketio import *
from jinja2 import *
import mlab
from models.collection import *

mlab.connect()

app = Flask(__name__)
app.secret_key = 'this key is secret'

app.config['SECRET_KEY'] = '123@#@45690@#'
socketio = SocketIO(app)

@socketio.on('connect', namespace = '/player')
def connect():
    print(request.sid)

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
    if 'loggedin' in session:
        username = session['loggedin']
    else:
        username = ""
    return render_template('index.html',username = username)

@app.route('/register',methods = ['GET','POST']) #methods la ten bat buoc
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form = request.form
        fullname = form['fullname']
        username = form['username']
        password = form['password']
        email = form['email']
        phonenumber = form['phonenumber']
        new_user = User(fullname = fullname,username = username, password = password,
                        email =email, phonenumber = phonenumber, role = 0, image ="", status = 1, message_status = 1 )
        # print(new_user.fullname)
        new_user.save()
        return redirect(url_for('index'))

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        print(username)
        print(password)
        #dùng để check thông tin thay cho vòng for vì vòng for bị ngắt khi gặp return
        user_data = User.objects(username = username) #xuất ra list chứa dictionary có key username = username

        if len(user_data) == 0: # check khi người dùng nhập sai
            flash("Khong ton tai username")
            return redirect(url_for("index"))
        else:
            for user in user_data: # dùng vòng for lấy dữ liệu khỏi list
                if user.password == password:
                    session['loggedin'] = username
                    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # return "{0}".format(session['loggedin']) # username truyen dc qua session
    del session['loggedin']
    return render_template('index.html')

@app.route('/update',methods=['GET','POST'])
def update():
    username = session['loggedin']
    user_data = User.objects(username = username)
    if request.method == "GET":
        for user in user_data:
            fullname = user['fullname']
            email = user['email']
            phonenumber = user['phonenumber']
            image = user['image']
        return render_template("update.html", fullname = fullname, email =email, phonenumber = phonenumber, image = image)
    elif request.method == "POST":
        form = request.form
        fullname = form['fullname']
        email = form['email']
        phonenumber = form['phonenumber']
        image = form['image']
        user_data.update(set__fullname = fullname,set__email = email, set__phonenumber = phonenumber, set__image = image)
        return redirect(url_for('update'),method ='GET')

@app.route('/roomcreate',methods=['GET','POST'])
def roomcreate():
    if request.method == "GET":
        return render_template("roomcreate.html")
    elif request.method =="POST":
        form = request.form
        title = form['title']
        description = form['description']
        password = form['password']
        image = form['image']
        new_room = Room(title = title, description = description, password = password, viewer = 0, image = image)
        new_room.save()
        return redirect(url_for('index'))

@app.route('/roomhost')
def roomhost():
    return render_template('roomhost.html')


# Send play and pause
@socketio.on('client-send-play-pause', namespace='/player')
def play_pause(data):
    emit('server-send-play-pause', data, broadcast = True)
    print(data)


@app.route('/player')
def player():
    return render_template('player.html')


if __name__ == '__main__':
    socketio.run(app, host= '127.0.0.1', port= 3000, debug = True)
