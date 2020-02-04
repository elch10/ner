import logging

import telegram
from telegram.ext import Updater, MessageHandler, Filters

import models

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def find_entities(update, context):
    text = update.message.text
    logging.info('Received text: ' + text)

    deeppavlov_res = models.pavlov_entities(text)
    pullenti_res = models.pullenti_entities(text)

    res = 'Модель 1:\n' + str(deeppavlov_res) + '\nМодель 2:\n' + str(pullenti_res)
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

with open('.tg_token') as f:
    token = f.read()

logging.info('Token was read')

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

ner_handler = MessageHandler(Filters.text, find_entities)
dispatcher.add_handler(ner_handler)

updater.start_polling()