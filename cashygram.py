#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from twilio.rest import Client
import time
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

NUMBERORCONTACT, NUMBER, BCHAMOUNT = range(3)

gl_number =0
gl_bchamount = 0


def start(bot, update):
    reply_keyboard = [['To Number', 'To Contact', 'Other']]

    update.message.reply_text(
        'Hi! My name is CashyGram Bot.  \n\n'
        'Send /cancel to stop talking to me.\n\n'
        'Shall we send a BCH payment to a phone Number or one of your Contacts?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return NUMBERORCONTACT


def numberorcontact(bot, update):
    user = update.message.from_user
    update.message.reply_text('Great! Please type the number to send BCH to, '
                              'or send /skip if you don\'t want to.')                          
    return NUMBER

def number(bot, update):
    user = update.message.from_user
    global gl_number 
    gl_number = update.message.text
    update.message.reply_text('Now please enter how much $USD would you '
                              'like to send in BCH to ' + gl_number)
    return BCHAMOUNT

def bchamount(bot, update):
    user = update.message.from_user
    global gl_bchamount 
    gl_bchamount= update.message.text
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = '<Twilio sid>'
    auth_token = '<Twilio auth>'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body='SEND $' + gl_bchamount + ' ' + gl_number,
            from_='<from number>',
            to='+17077776185'
        )
    print(message.sid)
    update.message.reply_text('All done! $' + gl_bchamount + ' sent to ' + gl_number + ', have a good day!')

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("674203199:AAEYDcHkp6GjWp8T6niIcl7lIjj9I-8bNDY")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NUMBERORCONTACT: [RegexHandler('^(To Number|To Contact|Other)$', numberorcontact)],
            NUMBER: [MessageHandler(Filters.text, number)],
            BCHAMOUNT: [MessageHandler(Filters.text, bchamount)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()

    updater.start_polling(poll_interval=0.1, timeout=60, clean=True, bootstrap_retries=-1, read_latency=2.0, allowed_updates=None)

    #try:

     #       updater.start_polling()

    #except Exception as err:

     #       logging.error(err)

      #      time.sleep(5)

       #     print "Internet error!"


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()