import os
from sklearn.externals import joblib
import logging

from telegram.ext import Updater, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token='756768931:AAHk6rE0E7Es7j73lPHnUn51oSJKW9KrfQ0')

current_dir = os.path.dirname(__file__)

tfidf = joblib.load(os.path.join(current_dir, "tfidf.pkl"))
clf = joblib.load(os.path.join(current_dir, "svm.pkl"))


def is_spam(text):
    transform = tfidf.transform((text,))
    predict = clf.predict(transform)
    return bool(predict[0] == 1)


def spam_handler(bot, update):
    message = update.message
    if is_spam(message.text):
        bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        bot.send_message(chat_id=update.message.chat_id, text="Message deleted, consider as spam")


dispatcher = updater.dispatcher

echo_handler = MessageHandler(Filters.text, spam_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
