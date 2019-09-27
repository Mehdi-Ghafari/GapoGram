#!/usr/bin/env python
# -*- coding: windows-1256 -*-

import logging
import os
import re

import cx_Oracle
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)

# region LOGGER
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

__level__ = logging.INFO
logger = logging.getLogger(__name__)

START = range(1)
GENDER, CHOOSING, PHOTO, LOCATION, BIO, TYPING_REPLY, TYPING_CHOICE = range(7)
__LOGDIR__ = os.path.abspath("log")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# endregion LOGGER

# region DB_INFO
db_ip = '172.17.0.2'
db_port = 1521
db_sid = 'ORCLPDB1'
dsn_tns = cx_Oracle.makedsn(db_ip, db_port, db_sid).replace('SID', 'SERVICE_NAME')
db_user = 'gapogram'
db_pass = 'Zz123456'


# endregion DB_INFO

# region OTHER_FUNC
def clean_array(in_list):
    regex = r"([\'\"\[\"])"
    regex2 = r"([\'\"\]\")])"
    matches = re.sub(regex, '\n', str(in_list))
    matches2 = re.sub(regex2, '\n', matches)
    v_rec_list = matches2.replace("\n", "")

    return v_rec_list


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


# endregion OTHER_FUNC

# region anonymous_connect_level1
def anonymous_btn(update, context):
    # print(str(update.callback_query.message.chat.id))
    # print(str(update.callback_query.message.message_id))
    # print(update.callback_query.answer())
    # print(type(update.callback_query.data))
    query = update.callback_query

    if query.data == '1':
        keyboard = [
            [InlineKeyboardButton("Option 100", callback_data='100')],
            [InlineKeyboardButton("Option 200", callback_data='200'),
             InlineKeyboardButton("Option 300", callback_data='300')],

            [InlineKeyboardButton("Option 400", callback_data='400')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_reply_markup(inline_message_id=update.callback_query.inline_message_id,
                                        reply_markup=reply_markup)

    elif query.data == '2':
        print(query.data)
    elif query.data == '3':
        print(query.data)
    elif query.data == '4':
        print(query.data)


# endregion anonymous_connect_level1

# region MainFunc
def main():
    updater = Updater("963128068:AAEBL6nhSsOlfRgNdiMEPWc6MkDBl8ARqDY", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    start_conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                             states={
                                                 START: [CommandHandler('start', start)]
                                             },
                                             fallbacks=[CommandHandler('cancel', cancel)]
                                             )

    dp.add_handler(start_conv_handler)

    dp.add_handler(CallbackQueryHandler(anonymous_btn))

    try:
        connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        cursor = connection.cursor()

        list_rep_res2 = []
        sql_rep_res2 = """
            SELECT trim(regexp_substr(BTNTEXT, '[^,]+', 1, LEVEL)) str_2_tab, callfunc
                FROM TBL_REPLYKEYBOARD
                CONNECT BY LEVEL <=
                    LENGTH(BTNTEXT) - 
                    LENGTH(REPLACE(BTNTEXT, ',', ''))
                    + 1
                """
        cursor.execute(sql_rep_res2)

        for result in cursor.fetchall():
            # list_rep_res2.append(result[0])
            print(result)
            dp.add_handler(MessageHandler(Filters.regex(result[0]), eval(result[1])))

        v_rec_list = clean_array(list_rep_res2)
        print(v_rec_list)

    except cx_Oracle.DatabaseError as e:
        logger.warning("CONNECT to database Not Ok")
        logger.error("Error Massage: " + str(e))

        return None

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


# endregion MainFunc

# region command/start
def start(update, context):
    try:
        connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        cursor = connection.cursor()

        list_rep_key2 = []
        sql_rep_key2 = """
                SELECT BTNTEXT FROM TBL_REPLYKEYBOARD WHERE MERGE = 1 AND VISIBLE = 0
                """
        cursor.execute(sql_rep_key2)
    except cx_Oracle.DatabaseError as e:
        logger.warning("CONNECT to database Not Ok")
        logger.error("Error Massage: " + str(e))
        return None

    for result in cursor.fetchall():
        list_rep_key2.append(result[0])
        # print(list)

    v_rec_list = clean_array(list_rep_key2)
    # print(v_rec_list)

    reply_keyboard_combine = v_rec_list.split(',')

    reply_keyboard_single = []
    sql_rep_key1 = """
            SELECT BTNTEXT FROM TBL_REPLYKEYBOARD WHERE MERGE = 0 AND VISIBLE = 0
            """
    cursor.execute(sql_rep_key1)

    for result in cursor.fetchall():
        reply_keyboard_single.append(result)
        # print(list)

    reply_keyboard_single.append(reply_keyboard_combine)
    #
    # print(type(reply_keyboard_single))
    # print(reply_keyboard_single)

    # print(type(reply_keyboard_single))

    sql_start_msg = """
            SELECT MSG_START FROM TBL_CONFIG WHERE ID = 1
            """
    cursor.execute(sql_start_msg)
    row_msg_cfg = cursor.fetchone()
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    print(reply_keyboard_single)

    if row_msg_cfg is not None:
        # print(row_msg_cfg[0])
        update.message.reply_text(
            str(row_msg_cfg[0]),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_single, one_time_keyboard=True, resize_keyboard=True))
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        # return GENDER
    else:
        print("nullable")

    cursor.close()
    connection.close()

    # return GENDER


# endregion command/start

# region command/echoMSG
def echoMSG(update, context):
    update.message.reply_text("hi")


# endregion command/echoMSG

# region command/anonymous_connect_level1
def anonymous_connect_level1(update, context):
    connection = cx_Oracle.connect(db_user, db_pass, dsn_tns)
    cursor = connection.cursor()

    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 2", callback_data='2'),
         InlineKeyboardButton("Option 3", callback_data='3')],

        [InlineKeyboardButton("Option 4", callback_data='4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    sql_chat_msg = """
                SELECT MSG_START FROM TBL_CONFIG WHERE ID = 2
                """
    cursor.execute(sql_chat_msg)

    row_msg_chat_cfg = cursor.fetchone()
    if row_msg_chat_cfg is not None:
        print(row_msg_chat_cfg[0])

        update.message.reply_text(str(row_msg_chat_cfg[0]), reply_markup=reply_markup)
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        # return GENDER
    else:
        print("nullable")

    cursor.close()
    connection.close()


# endregion command/echoMSG

# region command/profileName

# endregion command/profileName

if __name__ == '__main__':
    os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"
    main()
