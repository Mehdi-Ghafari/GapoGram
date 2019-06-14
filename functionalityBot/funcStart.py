import cx_Oracle
from telegram import ReplyKeyboardMarkup, error
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater

# region ora_database
# connection = cx_Oracle.connect('PYTHONDEMO', 'Zz123456', 'SHAHMERZA_PDB_SSL')
# endregion ora_database

# region telebot_static
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [
                  ['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']
                 ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# endregion telebot_static

def start(update, context):
    update.message.reply_text(
        "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
        "Why don't you tell me something about yourself?",
        reply_markup=markup)

    return CHOOSING

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END

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

def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING

def main():
    updater = Updater("425486741:AAHCZTY806ugaWHjc56cfqGHvcFTwfAkpE4", use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
                                      regular_choice,
                                      pass_user_data=True),
                       MessageHandler(Filters.regex('^Something else...$'),
                                      custom_choice),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
