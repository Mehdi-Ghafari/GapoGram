#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import cx_Oracle
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import sqlite3

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MENU, CONTACT, ABOUT = range(3)

def clean_array(in_list):
    regex = r"([\'\"\[\"])"
    regex2 = r"([\'\"\]\")])"
    matches = re.sub(regex, '\n', str(in_list))
    matches2 = re.sub(regex2, '\n', matches)
    v_rec_list = matches2.replace("\n", "")

    return v_rec_list

class dbhelper:

    def __init__(self, user_id):
        self.connection = cx_Oracle.connect('pdbadmin', 'Zz123456', 'PY_PDB')
        self.cursor = self.connection.cursor()
        self.user_id = user_id
        self.list_rep_key2 = []

    def set(self, state):
        q = "INSERT INTO STATES(USER_ID, STATE) VALUES (:obj1, :obj2)"

        return self.cursor.execute(q, obj1=self.user_id, obj2=state)

    def get_sql(self, sql):
        for result in self.cursor.execute(sql).fetchall():
            self.list_rep_key2.append(result[0])
            # print(list)

        v_rec_list = clean_array(self.list_rep_key2)

        return v_rec_list

    def get(self):
        q = "select * from states where user_id=:obj1"
        return self.cursor.execute(q, obj1=self.user_id,).fetchone()[0]

    def delete(self):
        q = "delete from states where user_id=:obj1"
        return self.cursor.execute(q, obj1=self.user_id,)

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

def start(bot, update):

    reply_button = [
        [
            InlineKeyboardButton('Contact', callback_data='contact'), InlineKeyboardButton('About', callback_data='about')
        ]
        ]
    reply_keyboard = InlineKeyboardMarkup(reply_button)

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=reply_keyboard)

    State = dbhelper(update.message.chat_id)
    State.set('MENU')
    State.close()

    return True

def menu_handler(bot, update):
    query = update.callback_query
    State = dbhelper(query.message.chat_id)
    state = State.get()
    logger.warning(state)


    reply_button = [
    [
        InlineKeyboardButton('Back', callback_data='back')
    ]
    ]
    reply_keyboard = InlineKeyboardMarkup(reply_button)
    data = query.data
    logger.warning(data)
    if data == "about":
        bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat_id, text="about", reply_markup=reply_keyboard)
        State.set('about')
        State.close()
    elif data == "contact":
        bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat_id, text="لطفا پیامی را برای ما بفرستید", reply_markup=reply_keyboard)
        State.set('contact')
        State.close()
        return True
    elif data == "back":
        reply_button = [
            [
                InlineKeyboardButton('Contact', callback_data='contact'), InlineKeyboardButton('About', callback_data='about')
            ]
            ]
        reply_keyboard = InlineKeyboardMarkup(reply_button)
    
        bot.edit_message_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Are you a boy or a girl?',
            reply_markup=reply_keyboard, message_id=query.message.message_id, chat_id=query.message.chat_id)
        return True

def message_handler(bot, update):
    State = dbhelper(update.message.chat_id)
    logger.warning("in message handler")
    state = State.get()
    if state == "contact":
        update.message.reply_text("پیام شما دریافت شد")
    else:
        update.message.reply_text("متوجه دستور شما نمی شوم")

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("425486741:AAHCZTY806ugaWHjc56cfqGHvcFTwfAkpE4")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(menu_handler))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"
    main()
