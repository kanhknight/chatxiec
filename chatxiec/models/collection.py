from mongoengine import *

    # design database


class User(Document):
        username = StringField()
        fullname = StringField()
        password = StringField()
        email = StringField()
        phonenumber = IntField()
        image = StringField()
        role = IntField()
        status = IntField()  # trạng thái cấm, ban,..
        message_status = IntField()


class Room(Document):
        title = StringField()
        description = StringField()
        password = StringField()
        viewer = IntField()
        video = IntField()
        image = StringField()

class Message(Document):
        userid = StringField()
        message = ListField()
        message_status = IntField() # trạng thái

class Video(Document):
        roomid = StringField()
        upcomming = ListField()
        videoimage = StringField()
        link = StringField()
        type = StringField()
