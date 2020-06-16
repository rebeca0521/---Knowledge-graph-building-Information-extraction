#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import configparser
import telegram
from flask import Flask, request
from telegram.ext import Updater,Dispatcher, MessageHandler, Filters, Updater, CommandHandler, InlineQueryHandler, CommandHandler
from fugle_realtime import intraday
from datetime import datetime,timedelta
import pandas as pd
import sys
import matplotlib.pyplot as plt
import time
import networkx as nx
import matplotlib.pyplot as plt


# In[2]:


# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
#bot = telegram.Bot(token=config['TELEGRAM']['ACCESS_TOKEN'])
api = '51714d20eae11ba0c9c9647cab45da4b'

@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

## reply message
def reply_handler(bot, update):
    text = update.message.text #使用者鍵入的值
    if text == '/start':
        d = pd.read_csv('成交金額前20大.csv',index_col=0)
        update.message.reply_text('請選擇下列其中一支股票：\n'+d.to_string(index=False))
    else:
        d = pd.read_csv('成交金額前20大.csv',index_col=0)
        d_l = list(d['symbol'])
        if text in d_l:
            text=text.split("/")[1]
            chat_id = update.message.chat_id
            update.message.reply_text('以下是最近一個月和'+text+'最相關的top5股票：')
            bot.send_photo(chat_id=chat_id, photo=open(str(text)+'.png', 'rb'))
            

        else:
            update.message.reply_text('I don\'t know what u want')
            


updater = Updater(token='1151794661:AAGbQ1sM7_XwhKfz8sw6aWBjVyX5q_DDdRY')


# This class dispatches all kinds of updates to its registered handlers.
#dispatcher = Dispatcher(bot, None)
updater.dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

# if __name__ == '__main__':
#     app.run()

updater.start_polling()
updater.idle()


# In[ ]:




