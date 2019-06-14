import telegram

bot = telegram.Bot('425486741:AAHCZTY806ugaWHjc56cfqGHvcFTwfAkpE4')

if bot.get_updates():
    chat_id = bot.get_updates()[-1].message.chat_id

    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    bot.send_message(chat_id=chat_id, text="Would you mind sharing your contact and location with me?",
                     reply_markup=reply_markup)

else:
    print("Empty list. Please, chat with the bot")