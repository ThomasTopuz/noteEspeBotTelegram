from telegram import *
from telegram.ext import *
from firebase import *

bot_api = '1598156271:AAE_TTOleZ7mKUpwtzNIbm22WnqtRSZs-nk'
bot = Bot(bot_api)
print (bot.get_me())
updater = Updater(bot_api, use_context=True)
dispatcher: Dispatcher = updater.dispatcher
ESPE_FATTO, NOTA_ESPE = range(2)


def start(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Benvenuto " + username + ", sono un bot per gestire le note dei tuoi espe settimanali!",
        parse_mode=ParseMode.HTML
    )


def espe_fatto_msg(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Inserisci l'espe che hai fatto oggi! materia | nota",
        parse_mode=ParseMode.HTML
    )
    return ESPE_FATTO


def espe_fatto_def(update: Update, context: CallbackContext):
    input = update.message.text
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="SEZIONE ESPE FATTO: " + input,
        parse_mode=ParseMode.HTML
    )


def registra_nota_msg(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Inserisci la nota: data | materia | nota',
        parse_mode=ParseMode.HTML
    )
    return NOTA_ESPE


def registra_nota_def(update: Update, context: CallbackContext):
    input = update.message.text
    print("foo")
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="SEZIONE INSERISCI NOTA: " + input,
        parse_mode=ParseMode.HTML
    )


# def registra_nota(update: Update, context: CallbackContext):
#    nota = update.message.text
#    data, materia, nota = nota.split()
#    push_nota((data, materia, nota))
#    bot.send_message(
#        chat_id=update.effective_chat.id,
#        text="Nota aggiunta con successo!",
#        parse_mode=ParseMode.HTML
#    )
#    return NOTA_ESPE
#

def lista_note(update: Update, context: CallbackContext):
    output = "Ecco le tue note: \n"
    output += get_note()
    bot.send_message(chat_id=update.effective_chat.id, text=output, parse_mode=ParseMode.HTML)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        NOTA_ESPE: [MessageHandler(Filters.text, registra_nota_def)],
        ESPE_FATTO: [MessageHandler(Filters.text, espe_fatto_def)]
    },
    fallbacks=[CommandHandler('cancel', start)],
)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('registranota', registra_nota_msg))
dispatcher.add_handler(CommandHandler('registraespefatto', espe_fatto_msg))
dispatcher.add_handler(CommandHandler('listanote', lista_note))
updater.start_polling()
