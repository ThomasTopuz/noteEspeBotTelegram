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
def push_test_done(test_done):
    now = datetime.now()
    data = {
        'data': now.strftime("%d.%m.%Y"),
        'materia': test_done['subject'],
        'nota': -1,
        "media": -1,
        "osservazioni_fatto": encrypt(test_done['observation']),
        'week_number': get_week_number(),
        'week_number_ricevuto': -1
    }
    db.child(test_done['username']).child('espe').push(data)


# set the grade and calculate average for a given test
def set_grade(test_received):
    # calculate average grade for a school subject
    def calculate_average(subject, username, new_grade):
        tests_done = db.child(username).child('espe').order_by_child(
            'materia').equal_to(subject).get().val()
        count = float(len(tests_done) + 1)
        sum_grade = float(new_grade)
        for i in tests_done:
            if (tests_done[i]['nota']) != -1:
                sum_grade += float(decrypt(str((tests_done[i]['nota']))))
            else:
                count -= 1
        return round(float(sum_grade / count), 2)

    username = test_received['username']
    grade = test_received['grade']
    test_id = test_received['test_id']
    subject = db.child(username).child(
        'espe').child(test_id).get().val()['materia']
    media = calculate_average(subject, username, grade)
    db.child(username).child('espe').child(test_id).update(
        {
            "nota": encrypt(str(grade)),
            "media": encrypt(str(media)),
            'week_number_ricevuto': get_week_number(),
            'osservazioni_ricevuto': encrypt(test_received['observation'])
        }
    )


# GETTERS

# get all test without a grade (unset)
def get_test_without_grade(username):
    return db.child(username).child('espe').order_by_child('nota').equal_to(-1).get()


# get the test made the current week
def get_tests_done(username):
    tests = db.child(username).child('espe').order_by_child('week_number') \
        .equal_to(get_week_number()).get()
    return db.sort(tests, "data")


# get tests received the current week
def get_test_received_curr_week(username):
    tests = db.child(username).child('espe').order_by_child('week_number_ricevuto').equal_to(get_week_number()) \
        .get()
    return db.sort(tests, "data")


# UTILITY

#  get current week number
def get_week_number():
    return datetime.now().isocalendar()[1]


# get user informations, email, year, fullname
def get_user_info(username):
    return db.child(username).child('info').get().val()


# get school subject for a given year
def get_subjects_by_year(anno):
    return db.child("materie").child(anno).get().val().split(';')
