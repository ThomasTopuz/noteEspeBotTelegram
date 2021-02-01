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
        "media": -1,
        'week_number': get_week_number(),
        'week_number_ricevuto': -1
    }
    db.child(username).child('espe').push(data)


# calcola la media
def calcola_media(materia, username, nuova_nota):
    espe_fatti = db.child(username).child('espe').order_by_child('materia').equal_to(materia).get().val()
    count = float(len(espe_fatti) + 1)
    sum_note = float(nuova_nota)
    for i in espe_fatti:
        if espe_fatti[i]['nota'] != -1:
            sum_note += float((espe_fatti[i]['nota']))
        else:
            count -= 1
    return round(float(sum_note / count), 2)


def add_nota(nota, espe_id, username):
    materia = db.child(username).child('espe').child(espe_id).get().val()['materia']
    media = calcola_media(materia, username, nota)
    db.child(username).child('espe').child(espe_id).update(
        {
            "nota": nota,
            "media": media,
            'week_number_ricevuto': get_week_number()
        }
    )


# GET
# per registrare la nota
def get_espe_senza_nota(username):
    return db.child(username).child('espe').order_by_child('nota').equal_to(-1).get()


# espe fatti della settimana corrente
def get_espe_fatti(username):
    return db.child(username).child('espe').order_by_child('week_number') \
        .equal_to(get_week_number()).get()


# espe ritornati la settimana corrente
def get_espe_ritornati(username):
    return db.child(username).child('espe').order_by_child('week_number_ricevuto').equal_to(get_week_number()).get()


def get_week_number():
    return datetime.now().isocalendar()[1]


def get_user_info(username):
    return db.child(username).child('info').get().val()
