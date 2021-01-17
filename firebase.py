import pyrebase
fireBaseConfig = {
    'apiKey': "AIzaSyD1XfInWrTrS3RpmCQzqNJJu-jiHH8Ores",
    'authDomain': "noteespebot.firebaseapp.com",
    'projectId': "noteespebot",
    'storageBucket': "noteespebot.appspot.com",
    'messagingSenderId': "298424559882",
    'appId': "1:298424559882:web:579508cdcd81fea1faf2f3",
    "databaseURL":"https://noteespebot-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(fireBaseConfig)
auth = firebase.auth()
db = firebase.database()


def push_nota(nota):
    data  = {
        'data': nota[0],
        'materia': nota[1],
        'nota': nota[2]
    }
    db.child('note').push(data)


def get_note():
    output = ""
    data = db.child("note").get()
    for i in data:
        for j in i.val().keys():
            output += i.val()[j] + " "
        output += "\n"
    return output
