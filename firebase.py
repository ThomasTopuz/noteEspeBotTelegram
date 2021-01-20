import pyrebase
from datetime import datetime

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


def push_espe_fatto(materia):
    now = datetime.now()
    data = {
        'data': now.strftime("%m/%d/%Y"),
        'materia': materia,
        'nota': -1
    }
    db.child('espe').push(data)


def add_nota(nota, espe_id):
    db.child('espe').child(espe_id).update({"nota": nota})


def get_note():
    espe = db.child('espe').get()
    print(espe)
    return espe


def get_espe_senza_nota():
    return db.child('espe').order_by_child('nota').equal_to(-1).get()
