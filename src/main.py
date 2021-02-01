from telegram import *
from telegram.ext import *
import firebase as fb

bot_api = '1598156271:AAE_TTOleZ7mKUpwtzNIbm22WnqtRSZs-nk'
bot = Bot(bot_api)
print('running...')

updater = Updater(bot_api, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

# global vars
mod = ""
espe_id = ""

materie = {
    'Thomastopuz': (
        'm122', 'm226A', 'm226B', 'm153', 'm411', 'matematica', 'fisica', 'inglese', 'tedesco', 'italiano', 'storia'),

    'Emilijadaceva': (
        'm120', 'm133', 'm152', 'm306', 'm326', 'Fise', 'matematica', 'fisica', 'chimica', 'tedesco', 'italiano',
        'inglese'),

    'Amandamarchetti': ('m150', 'm151', 'm155', 'm183', 'm242', 'matematica', 'fisica', 'chimica', 'tedesco'),
}


def start(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Benvenuto " + username + ", sono un bot per gestire le note dei tuoi espe settimanali! " +
             "usa / per inserire un comando.",
        parse_mode=ParseMode.HTML
    )


def espe_fatto_msg(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    keyboard = [
        [InlineKeyboardButton(i, callback_data=i)] for i in materie[username]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Scegli la materia dell'espe che hai fatto oggi!", reply_markup=reply_markup)
    global mod
    mod = "ESPE"


def registra_nota_msg(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    espe_senza_nota = fb.get_espe_senza_nota(username)
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
        materia = update.callback_query.data
        fb.push_espe_fatto(materia, username)
        update.callback_query.edit_message_text("Espe registrato con successo!")
        mod = ""
    # scelta dell espe (materia e data) di cui si ha ricevuto la nota
    elif mod == "NOTA":
        query = update.callback_query
        global espe_id
        espe_id = query.data
        query.edit_message_text("Inserisci la nota che hai preso di questo test.")


def user_input_handler(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    user_input = update.message.text.lower()
    global mod
    if mod == "NOTA":
        nota = user_input
        global espe_id
        fb.add_nota(nota, espe_id, username)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Nota registrata con successo!",
            parse_mode=ParseMode.HTML
        )
        mod = ""
        espe_id = ""


def lista_note(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    espe_fatti = fb.get_espe_fatti(username)
    espe_ritornati = fb.get_espe_ritornati(username)
    output = "PANORAMICA SETTIMANALE: \n \n \n"
    output += "ESPE CHE HAI FATTO: \n \n" if len(espe_fatti.val()) > 0 else "0 ESPE FATTI \n \n"
    output += format_data(espe_fatti, ["data", "materia"])
    output += "ESPE CHE HAI RICEVUTO: \n \n" if len(espe_ritornati.val()) > 0 else "0 ESPE RITORNATI"
    output += format_data(espe_ritornati, ["data", "materia", "nota"])

    bot.send_message(chat_id=update.effective_chat.id,
                     text=output, parse_mode=ParseMode.HTML)


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


dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, user_input_handler))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('insights', lista_note))
dispatcher.add_handler(CommandHandler('registra_espe', espe_fatto_msg))
dispatcher.add_handler(CommandHandler('registra_nota', registra_nota_msg))
updater.dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_handler))

updater.start_polling()

# COMANDI BOTFAHTER
# start - inizia il bot
# registra_espe - registra un espe fatto oggi
# registra_nota - registra una nota di un espe fatto
# lista_nota - insights di questa settimana
# genera_documento - genera il file word
