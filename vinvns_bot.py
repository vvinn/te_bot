#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from resource import *
import socket
import time
from datetime import date
import logging
import redis
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

"""Start the bot."""
# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(tokens, use_context=True)
r = redis.Redis(host='localhost', port=6379, db=0) # connection to the databse

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def morning(context: CallbackContext):
    message = "Good Morning! Have a nice day!"
    db_keys = r.keys(pattern="*")    
        # send message to all users
    for keys in db_keys:
        id = r.get(keys).decode("UTF-8")
        context.bot.send_message(chat_id=id, text=message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
#    update.message.reply_text('Hi!')
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    r.set(user_name, user_id)
    message = 'Welcome to the bot'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    j = updater.job_queue
    j.run_once(morning, 30)



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    if update.message.text == 'time':
        today = date.today()
        update.message.reply_text(r.get(str(today)).decode("UTF-8"))
    else:
        update.message.reply_text(update.message.text)

def gettime(update, context):
    """ time elasped for a day"""
    today = date.today()
    update.message.reply_text(r.get(str(today)).decode("UTF-8"))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    while not is_connected():
        time.sleep(50)

    time.sleep(5)
    bot = telegram.Bot(token=tokens)
    bot.send_message(chat_id=chat_ids, text='Hi I am up........!')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    dp.add_handler(CommandHandler("time", gettime))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
