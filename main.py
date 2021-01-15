from telegram import *
from telegram.ext import *
import pyrebase
from firebase import *

bot_api = '1598156271:AAE_TTOleZ7mKUpwtzNIbm22WnqtRSZs-nk'
bot = Bot(bot_api)
print(bot.get_me())
updater = Updater(bot_api, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

userInput = ''
sumNumeri = 0
chat_id = ''
notaInserita = ''


def start(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Benvenuto, sono un bot per gestire le note dei tuoi espe settimanali!',
        parse_mode=ParseMode.HTML
    )


def registra_nota_msg(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Inserisci la nota: data | materia | nota',
        parse_mode=ParseMode.HTML
    )


def registra_nota(update: Update, context: CallbackContext):
    nota = update.message.text
    print(nota)
    data, materia, nota = nota.split()
    push_nota((data, materia, nota))
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Nota aggiunta con successo!",
        parse_mode=ParseMode.HTML
    )


def lista_note(update: Update, context: CallbackContext):
    data = db.child("note")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('registranota', registra_nota_msg))
dispatcher.add_handler(CommandHandler('listanote', lista_note))
updater.dispatcher.add_handler(MessageHandler(Filters.text, registra_nota))
updater.start_polling()
