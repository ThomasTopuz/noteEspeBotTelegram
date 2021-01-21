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


def start(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Benvenuto " + username + ", sono un bot per gestire le note dei tuoi espe settimanali! " +
             "usa / per inserire un comando.",
        parse_mode=ParseMode.HTML
    )


def espe_fatto_msg(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Inserisci la materia dell'espe che hai fatto oggi!",
        parse_mode=ParseMode.HTML
    )
    global mod
    mod = "ESPE"


def registra_nota_msg(update: Update, context: CallbackContext):
    espe_senza_nota = fb.get_espe_senza_nota()
    keyboard = [
        [InlineKeyboardButton(str(espe_senza_nota.val()[i]['materia'] + "  |  " + espe_senza_nota.val()[i]['data']),
                              callback_data=str(i))] for i in espe_senza_nota.val()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Di quale espe vuoi registrare la nota?', reply_markup=reply_markup)
    global mod
    mod = "NOTA"


def inserisci_nota(update: Update, context: CallbackContext):
    query = update.callback_query
    global espe_id
    espe_id = query.data
    query.edit_message_text("Inserisci la nota che hai preso di questo test.")


def user_input_handler(update: Update, context: CallbackContext):
    user_input = update.message.text
    global mod
    print(mod)
    if mod == "ESPE":
        materia = user_input
        fb.push_espe_fatto(materia)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Espe registrato con successo!",
            parse_mode=ParseMode.HTML
        )
    elif mod == "NOTA":
        nota = user_input
        global espe_id
        fb.add_nota(nota, espe_id)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Nota registrata con successo!",
            parse_mode=ParseMode.HTML
        )
        mod = ""
        espe_id = ""


def lista_note(update: Update, context: CallbackContext):
    espe_senza_nota = fb.get_espe_senza_nota()
    espe_con_nota = fb.get_espe_con_note()

    print(len(espe_con_nota.val()))


    output = "Ecco gli espe che hai fatto: \n" if len(espe_senza_nota.val())>0 else "non ci sono espe senza nota"
    output += format_data(fb.get_espe_senza_nota())
    output += "Ecco gli espe di cui hai ricevuto la nota: \n"
    output += format_data(fb.get_espe_con_note())
    print('foo')
    bot.send_message(chat_id=update.effective_chat.id,
                     text=output, parse_mode=ParseMode.HTML)


def format_data(data):
    output = ""
    for i in data:
        print(i)
        for j in i.val().keys():
            output += str(i.val()[j]) + " | "
        output += "\n"
    return output


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('lista_note', lista_note))
dispatcher.add_handler(CommandHandler('registra_espe', espe_fatto_msg))
dispatcher.add_handler(CommandHandler('registra_nota', registra_nota_msg))
updater.dispatcher.add_handler(CallbackQueryHandler(inserisci_nota))
dispatcher.add_handler(MessageHandler(Filters.text, user_input_handler))


updater.start_polling()

# COMANDI BOTFAHTER
# start - inizia il bot
# registra_espe - registra un espe fatto oggi
# registra_nota - registra una nota di un espe fatto
# lista_nota - insights di questa settimana
# genera_documento - genera il file word
