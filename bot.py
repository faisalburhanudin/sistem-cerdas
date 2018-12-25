import logging

from telegram.ext import Updater, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token='756768931:AAHk6rE0E7Es7j73lPHnUn51oSJKW9KrfQ0')


def spam_handler(bot, update):
    message = update.message
    if 'spam' in message.text:
        bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        bot.send_message(chat_id=update.message.chat_id, text="Message deleted, consider as spam")


dispatcher = updater.dispatcher

echo_handler = MessageHandler(Filters.text, spam_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
