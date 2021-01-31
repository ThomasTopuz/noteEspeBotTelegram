import pyrebase
from datetime import datetime

fireBaseConfig = {
    'apiKey': "AIzaSyD1XfInWrTrS3RpmCQzqNJJu-jiHH8Ores",
    'authDomain': "noteespebot.firebaseapp.com",
    'projectId': "noteespebot",
    'storageBucket': "noteespebot.appspot.com",
    'messagingSenderId': "298424559882",
    'appId': "1:298424559882:web:579508cdcd81fea1faf2f3",
    "databaseURL": "https://noteespebot-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(fireBaseConfig)
auth = firebase.auth()
db = firebase.database()


def push_espe_fatto(materia, username):
    now = datetime.now()
    data = {
        'data': now.strftime("%m/%d/%Y"),
        'materia': materia,
        'nota': -1,
        'week_number': get_week_number(),
        'week_number_ricevuto': -1
    }
    db.child(username).child('espe').push(data)


def add_nota(nota, espe_id, username):
    db.child(username).child('espe').child(espe_id).update(
        {
            "nota": nota,
            'week_number_ricevuto': get_week_number()
        }
    )
# per registrare la nota
def get_espe_senza_nota(username):
    return db.child(username).child('espe').order_by_child('nota').equal_to(-1).get()


# espe fatti della settimana corrente
def get_espe_fatti(username):
    return db.child(username).child('espe').order_by_child('week_number')\
        .equal_to(get_week_number()).get()


# espe ritornati la settimana corrente
def get_espe_ritornati(username):
    return db.child(username).child('espe').order_by_child('week_number_ricevuto').equal_to(get_week_number()).get()


def get_week_number():
    return datetime.now().isocalendar()[1]
