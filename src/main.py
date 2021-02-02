from telegram import *
from telegram.ext import *
import firebase as fb
from wordGenerator import *
from send_email import send_email

bot_api = '1598156271:AAE_TTOleZ7mKUpwtzNIbm22WnqtRSZs-nk'
bot = Bot(bot_api)
print('running...')

updater = Updater(bot_api, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

# global vars
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

materie = {
    'JoeKung': (
        'm100', 'm101', 'm104', 'm114', 'm117', 'm123', 'm213', 'm214', 'm304', 'm305', 'm403', 'm404', 'm431', 'Fise',
        'Economia aziendale', 'matematica', 'fisica', 'inglese', 'tedesco', 'italiano', 'storia', 'economia e diritto'),
    'Thomastopuz': (
        'm122', 'm226A', 'm226B', 'm153', 'm411', 'economia aziendale', 'matematica', 'fisica', 'inglese', 'tedesco',
        'italiano', 'storia', 'economia e diritto'),

    'EmilijaDaceva': (
        'm120', 'm133', 'm152', 'm306', 'm326', 'Fise', 'matematica', 'fisica', 'chimica', 'tedesco', 'italiano',
        'inglese'),

    'Amandamarchetti': ('m150', 'm151', 'm155', 'm183', 'm242', 'matematica', 'fisica', 'chimica', 'tedesco'),
}


def start(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    update.message.reply_text("Benvenuto " + fb.get_user_info(username)[
        'fullname'] + ", sono un bot per gestire le note dei tuoi espe settimanali! " +
                              "usa / per inserire un comando.")


def nuovo_espe(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    keyboard = [
        [InlineKeyboardButton(i, callback_data=i)] for i in materie[username]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Scegli la materia dell'espe che hai fatto oggi!", reply_markup=reply_markup)
    global mod
    mod = "ESPE"


def registra_nota(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    espe_senza_nota = fb.get_espe_senza_nota(username)
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


def inline_keyboard_handler(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    # scelta della materia dell espe fatto
    global mod
    if mod == "ESPE":
        global espe_fatto
        espe_fatto['materia'] = update.callback_query.data
        update.callback_query.edit_message_text("Adesso inserisci un osservazione:")
        mod = "OSSERVAZIONI_FATTO"
    # scelta dell espe (materia e data) di cui si ha ricevuto la nota
    elif mod == "NOTA":
        query = update.callback_query
        global espe_ricevuto
        espe_ricevuto['espe_id'] = query.data
        espe_ricevuto['username'] = username
        query.edit_message_text("Inserisci la nota che hai preso di questo test.")


def user_text_input_handler(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    user_input = update.message.text.lower()
    global mod
    global espe_ricevuto
    if mod == "NOTA":
        nota = user_input
        # global espe_ricevuto
        espe_ricevuto['nota'] = nota
        update.message.reply_text("Inserisci una osservazione:")
        mod = "OSSERVAZIONI_RICEVUTO"
    elif mod == "OSSERVAZIONI_FATTO":
        global espe_fatto
        espe_fatto['osservazioni'] = user_input
        espe_fatto['username'] = username
        fb.push_espe_fatto(espe_fatto)
        update.message.reply_text("Espe registrato con successo!")
    elif mod == "OSSERVAZIONI_RICEVUTO":
        # global espe_ricevuto
        espe_ricevuto['osservazioni'] = user_input
        fb.add_nota(espe_ricevuto)
        update.message.reply_text("Nota registrata con successo!")


def insights(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    espe_fatti = fb.get_espe_fatti(username)
    espe_ritornati = fb.get_espe_ritornati(username)
    output = "PANORAMICA SETTIMANALE: \n \n \n"
    output += "ESPE CHE HAI FATTO: \n \n" if len(espe_fatti.val()) > 0 else "0 ESPE FATTI \n \n"
    output += format_data(espe_fatti, ["data", "materia"])
    output += "ESPE CHE HAI RICEVUTO: \n \n" if len(espe_ritornati.val()) > 0 else "0 ESPE RITORNATI"
    output += format_data(espe_ritornati, ["data", "materia", "nota"])
    update.message.reply_text(output)


def generate_docx_and_send_email(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    fullname = fb.get_user_info(username)['fullname']
    filename = genera_docx(username, fullname)
    bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
    send_email(fullname, filename, fb.get_user_info(username)['email'])
    update.message.reply_text("La email è stata inviata sia a te che a Steve, buon week end!")
    elimina_file(filename)


def format_data(data, props):
    output = ""
    for i in data:
        espe = i.val()
        props_value = []
        for j in props:
            props_value.append(str(espe[j]))
        output += "  -  ".join(props_value)
        output += "\n"
    output += "\n\n\n"
    return output


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('nuovo_espe', nuovo_espe))
dispatcher.add_handler(CommandHandler('registra_nota', registra_nota))
dispatcher.add_handler(CommandHandler('insights', insights))
dispatcher.add_handler(CommandHandler('invia_email', generate_docx_and_send_email))

dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, user_text_input_handler))

updater.start_polling()

# COMANDI BOTFAHTER
# start - inizia il bot
# registra_espe - registra un espe fatto oggi
# registra_nota - registra una nota di un espe fatto
# insights - insights di questa settimana
# invia_email - genera il file word
