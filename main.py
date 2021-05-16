from telegram import *
from telegram.ext import *
from src.documentGenerator.wordGenerator import generate_docx, delete_file
from src.emailservice.send_email import send_email
from src.encryption.encrypter import decrypt
import os
from src.firebaseconnector.firebase import push_test_done, set_grade, get_user_info, get_tests_done, \
    get_test_without_grade, get_subjects_by_year, get_test_received_curr_week

# configure the bot
bot_api = os.environ['NOTEBOT_API'];
bot = Bot(bot_api)
print('NoteEspeBot running')

updater = Updater(bot_api, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

# global vars and objects
mode = ""

test_done = {
    'subject': '',
    'observation': '',
    'username': ''
}
test_received = {
    'test_id': '',
    'grade': '',
    'observation': '',
    'username': ''
}


# start handler (when starting a new chat with the bot)
def start(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    update.message.reply_text("Benvenuto " + get_user_info(username)[
        'fullname'] + ", sono un bot per gestire le note dei tuoi espe settimanali! " +
                              "usa / per inserire un comando.")


# nuovo_espe command handler
def new_test(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    year = get_user_info(username)['anno']
    subjects = get_subjects_by_year(year)

    keyboard = [
        [InlineKeyboardButton(i, callback_data=i)] for i in subjects
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Scegli la materia dell'espe che hai fatto oggi!", reply_markup=reply_markup)
    global mode
    mode = "NEW_TEST"


# registra_nota command handler
def register_grade(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    tests_without_grade = get_test_without_grade(username)
    if len(tests_without_grade.val()) == 0:
        update.message.reply_text("Non hai note da registrare.")
        return
    keyboard = [
        [InlineKeyboardButton(
            str(tests_without_grade.val()[i]['materia'] + "  |  " + tests_without_grade.val()[i]['data']),
            callback_data=str(i))] for i in tests_without_grade.val()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Di quale espe vuoi registrare la nota?', reply_markup=reply_markup)
    global mode
    mode = "TEST_RECEIVED"


# handler for the list click event (when selecting a school subject or a past test)
# acts differently depending on the mode (modee) variable
def inline_keyboard_handler(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    # choose the school subject to registrate a test for
    global mode
    if mode == "NEW_TEST":
        global test_done
        test_done['subject'] = update.callback_query.data
        update.callback_query.edit_message_text("Adesso inserisci un osservazione:")
        mode = "OBSERVATION_DONE"
    # choose the test you want to set the grade
    elif mode == "TEST_RECEIVED":
        query = update.callback_query
        global test_received
        test_received['test_id'] = query.data
        test_received['username'] = username
        query.edit_message_text("Inserisci la nota che hai preso di questo test.")


# generic user text input handler, acts differently depending on the mode variable
def user_text_input_handler(update: Update, context: CallbackContext):
    global mode
    if mode == "":
        update.message.reply_text("Scusa, non ho capito le tue intenzioni :(")

    username = update.effective_chat.username
    user_input = update.message.text.lower()
    global test_received
    # grade input
    if mode == "TEST_RECEIVED":
        grade = user_input
        try:
            float(grade)
        except ValueError:
            update.message.reply_text("Per favore inserisci un compreso tra 1 e 6")
            return

        if float(grade) < 1 or float(grade) > 6:
            update.message.reply_text("Per favore inserisci un compreso tra 1 e 6!")
            return

        # global test_received
        test_received['grade'] = grade
        update.message.reply_text("Inserisci una osservazione:")
        mode = "OBSERVATION_RECEIVED"
    # observation input (when test register)
    elif mode == "OBSERVATION_DONE":
        global test_done
        test_done['observation'] = user_input
        test_done['username'] = username
        push_test_done(test_done)
        update.message.reply_text("Espe registrato con successo!")
        mode = ""
    # observation input (when test received)
    elif mode == "OBSERVATION_RECEIVED":
        # global test_received
        test_received['observation'] = user_input
        set_grade(test_received)
        update.message.reply_text("Nota registrata con successo!")
        mode = ""


# insights command handler, gives week insight
def insights(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    tests_done = get_tests_done(username)
    tests_received = get_test_received_curr_week(username)
    output = "PANORAMICA SETTIMANALE: \n \n \n"
    output += "ESPE CHE HAI FATTO: \n \n" if len(tests_done.val()) > 0 else "0 ESPE FATTI \n \n"
    output += format_data(tests_done, ["data", "materia"])
    output += "ESPE CHE HAI RICEVUTO: \n \n" if len(tests_received.val()) > 0 else "0 ESPE RITORNATI"
    output += format_data(tests_received, ["data", "materia", "nota"])
    update.message.reply_text(output)


# invia_email handler, generates the docx file and send the email via smtp to the trainer
def generate_docx_and_send_email(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    fullname = get_user_info(username)['fullname']
    filename = generate_docx(username, fullname)
    bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
    send_email(fullname, filename, get_user_info(username)['email'])
    update.message.reply_text("La email è stata inviata sia a te che a Steve, buon week end!")
    delete_file(filename)


# firebase data formatter, returns a formatted string
def format_data(data, props):
    output = ""
    for i in data:
        test = i.val()
        props_value = []
        for j in props:
            if j == "nota":
                props_value.append(decrypt(str(test[j])))
            else:
                props_value.append(str(test[j]))
        output += "  -  ".join(props_value)
        output += "\n"
    output += "\n\n\n"
    return output


# command handler mapping
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('nuovo_espe', new_test))
dispatcher.add_handler(CommandHandler('registra_nota', register_grade))
dispatcher.add_handler(CommandHandler('insights', insights))
dispatcher.add_handler(CommandHandler('invia_email', generate_docx_and_send_email))
dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, user_text_input_handler))

# start polling (checks for updates on telegram's server)
updater.start_polling()
