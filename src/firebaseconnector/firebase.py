import pyrebase
from datetime import datetime
from src.encryption.encrypter import encrypt, decrypt

# firebase project initialization with configuration dictionary
firebase = pyrebase.initialize_app({
    'apiKey': "AIzaSyD1XfInWrTrS3RpmCQzqNJJu-jiHH8Ores",
    'authDomain': "noteespebot.firebaseapp.com",
    'databaseURL': "https://noteespebot-default-rtdb.firebaseio.com",
    'projectId': "noteespebot",
    'storageBucket': "noteespebot.appspot.com",
    'messagingSenderId': "298424559882",
    'appId': "1:298424559882:web:579508cdcd81fea1faf2f3"
})
db = firebase.database()


# push a test to firebase realtime database
def push_espe_fatto(espe_fatto):
    now = datetime.now()
    data = {
        'data': now.strftime("%d.%m.%Y"),
        'materia': espe_fatto['materia'],
        'nota': -1,
        "media": -1,
        "osservazioni_fatto": encrypt(espe_fatto['osservazioni']),
        'week_number': get_week_number(),
        'week_number_ricevuto': -1
    }
    db.child(espe_fatto['username']).child('espe').push(data)


# set the grade and calculate average for a given test
def add_nota(espe_ricevuto):
    # calculate average grade for a school subject
    def calcola_media(materia, username, nuova_nota):
        espe_fatti = db.child(username).child('espe').order_by_child(
            'materia').equal_to(materia).get().val()
        count = float(len(espe_fatti) + 1)
        sum_note = float(nuova_nota)
        for i in espe_fatti:
            if (espe_fatti[i]['nota']) != -1:
                sum_note += float(decrypt(str((espe_fatti[i]['nota']))))
            else:
                count -= 1
        return round(float(sum_note / count), 2)

    username = espe_ricevuto['username']
    nota = espe_ricevuto['nota']
    espe_id = espe_ricevuto['espe_id']
    materia = db.child(username).child(
        'espe').child(espe_id).get().val()['materia']
    media = calcola_media(materia, username, nota)
    db.child(username).child('espe').child(espe_id).update(
        {
            "nota": encrypt(str(nota)),
            "media": encrypt(str(media)),
            'week_number_ricevuto': get_week_number(),
            'osservazioni_ricevuto': encrypt(espe_ricevuto['osservazioni'])
        }
    )


# GETTERS

# get all test without a grade (unset)
def get_espe_senza_nota(username):
    return db.child(username).child('espe').order_by_child('nota').equal_to(-1).get()


# get the test made the current week
def get_espe_fatti(username):
    return db.child(username).child('espe').order_by_child('week_number') \
        .equal_to(get_week_number()).get()


# espe ritornati la settimana corrente
def get_espe_ritornati(username):
    return db.child(username).child('espe').order_by_child('week_number_ricevuto').equal_to(get_week_number()).get()


# UTILITY

#  get current week number
def get_week_number():
    return datetime.now().isocalendar()[1]


# get user informations, email, year, fullname
def get_user_info(username):
    return db.child(username).child('info').get().val()


# get school subject for a given year
def get_materie_by_anno(anno):
    return db.child("materie").child(anno).get().val().split(';')
