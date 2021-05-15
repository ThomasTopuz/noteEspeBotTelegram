from telegram import *
from telegram.ext import *
from src.firebaseconnector.firebase import *
from src.documentGenerator.wordGenerator import *
from src.emailservice.send_email import send_email
import os

# configure the bot
bot_api = os.environ['NOTEBOT_API'];
bot = Bot(bot_api)
print('NoteEspeBot running')

updater = Updater(bot_api, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

# global vars and objects
mod = ""

espe_fatto = {
    'materia': '',
    'osservazioni': '',
    'username': ''
}
espe_ricevuto = {
    'espe_id': '',
    'nota': '',
    'osservazioni': '',
    'username': ''
}


# start handler (when starting a new chat with the bot)
def start(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    update.message.reply_text("Benvenuto " + get_user_info(username)[
        'fullname'] + ", sono un bot per gestire le note dei tuoi espe settimanali! " +
                              "usa / per inserire un comando.")


# nuovo_espe command handler
def nuovo_espe(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    anno = get_user_info(username)['anno']
    materie = get_materie_by_anno(anno)

    keyboard = [
        [InlineKeyboardButton(i, callback_data=i)] for i in materie
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Scegli la materia dell'espe che hai fatto oggi!", reply_markup=reply_markup)
    global mod
    mod = "ESPE"


# registra_nota command handler
def registra_nota(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    espe_senza_nota = get_espe_senza_nota(username)
    if len(espe_senza_nota.val()) == 0:
        update.message.reply_text("Non hai più note da registrare.")
        return
    keyboard = [
        [InlineKeyboardButton(str(espe_senza_nota.val()[i]['materia'] + "  |  " + espe_senza_nota.val()[i]['data']),
                              callback_data=str(i))] for i in espe_senza_nota.val()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Di quale espe vuoi registrare la nota?', reply_markup=reply_markup)
    global mod
    mod = "NOTA"


# handler for the list click event (when selecting a school subject or a past test)
# acts differently depending on the mod (mode) variable
def inline_keyboard_handler(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    # choose the school subject to registrate a test for
    global mod
    if mod == "ESPE":
        global espe_fatto
        espe_fatto['materia'] = update.callback_query.data
        update.callback_query.edit_message_text("Adesso inserisci un osservazione:")
        mod = "OSSERVAZIONI_FATTO"
    # choose the test you want to set the grade
    elif mod == "NOTA":
        query = update.callback_query
        global espe_ricevuto
        espe_ricevuto['espe_id'] = query.data
        espe_ricevuto['username'] = username
        query.edit_message_text("Inserisci la nota che hai preso di questo test.")


# generic user text input handler, acts differently depending on the mod variable
def user_text_input_handler(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    user_input = update.message.text.lower()
    global mod
    global espe_ricevuto
    # grade input
    if mod == "NOTA":
        nota = user_input
        try:
            float(nota)
        except ValueError:
            update.message.reply_text("Per favore inserisci un compreso tra 1 e 6")
            return

        if float(nota) < 1 or float(nota) > 6:
            update.message.reply_text("Per favore inserisci un compreso tra 1 e 6!")
            return

        # global espe_ricevuto
        espe_ricevuto['nota'] = nota
        update.message.reply_text("Inserisci una osservazione:")
        mod = "OSSERVAZIONI_RICEVUTO"
    # observation input (when test register)
    elif mod == "OSSERVAZIONI_FATTO":
        global espe_fatto
        espe_fatto['osservazioni'] = user_input
        espe_fatto['username'] = username
        push_espe_fatto(espe_fatto)
        update.message.reply_text("Espe registrato con successo!")
    # observation input (when test received)
    elif mod == "OSSERVAZIONI_RICEVUTO":
        # global espe_ricevuto
        espe_ricevuto['osservazioni'] = user_input
        add_nota(espe_ricevuto)
        update.message.reply_text("Nota registrata con successo!")


# insights command handler, gives week insight
def insights(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    espe_fatti = get_espe_fatti(username)
    espe_ritornati = get_espe_ritornati(username)
    output = "PANORAMICA SETTIMANALE: \n \n \n"
    output += "ESPE CHE HAI FATTO: \n \n" if len(espe_fatti.val()) > 0 else "0 ESPE FATTI \n \n"
    output += format_data(espe_fatti, ["data", "materia"])
    output += "ESPE CHE HAI RICEVUTO: \n \n" if len(espe_ritornati.val()) > 0 else "0 ESPE RITORNATI"
    output += format_data(espe_ritornati, ["data", "materia", "nota"])
    update.message.reply_text(output)


# invia_email handler, generates the docx file and send the email via smtp to the trainer
def generate_docx_and_send_email(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    fullname = get_user_info(username)['fullname']
    filename = genera_docx(username, fullname)
    bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
    send_email(fullname, filename, get_user_info(username)['email'])
    update.message.reply_text("La email è stata inviata sia a te che a Steve, buon week end!")
    elimina_file(filename)


# firebase data formatter, returns a formatted string
def format_data(data, props):
    output = ""
    for i in data:
        espe = i.val()
        props_value = []
        for j in props:
            if j == "nota":
                props_value.append(decrypt(str(espe[j])))
            else:
                props_value.append(str(espe[j]))
        output += "  -  ".join(props_value)
        output += "\n"
    output += "\n\n\n"
    return output


# command handler mapping
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('nuovo_espe', nuovo_espe))
dispatcher.add_handler(CommandHandler('registra_nota', registra_nota))
dispatcher.add_handler(CommandHandler('insights', insights))
dispatcher.add_handler(CommandHandler('invia_email', generate_docx_and_send_email))
dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, user_text_input_handler))

# start polling (checks for updates on telegram's server)
updater.start_polling()
