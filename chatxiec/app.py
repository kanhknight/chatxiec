from flask import *
from flask_socketio import *
import mlab
from models.collection import User

mlab.connect()

app = Flask(__name__)
app.secret_key = 'this key is secret'

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

        #dùng để check thông tin thay cho vòng for vì vòng for bị ngắt khi gặp return
        user_data = User.objects(username = username) #xuất ra list chứa dictionary có key username = username

        if len(user_data) == 0: # check khi người dùng nhập sai
            flash("Khong ton tai username")
            return redirect(url_for("login"))
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


if __name__ == '__main__':
    socketio.run(app, host= '127.0.0.1', port= 3000, debug = True)
