from mongoengine import *

    #design database
    class User(document):
        username = StringField()
        fullname = StringField()
        password = StringField()
        email = StringField()
        phonenumber = IntField()
        image = StringField()
        role = IntField()
        status = IntField() # trạng thái cấm, ban,..
        message_status = IntField()

    class Room(document):
        title = StringField()
        description = StringField()
        password = StringField()
        viewer = IntField()
        video = IntField()
        image = StringField()
        upcomming = ListField()

    class Message(document):
        userid = StringField()
        message = ListField()
        message_status = IntField() # trạng thái
