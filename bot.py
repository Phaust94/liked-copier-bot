from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import os
os.chdir(os.path.join(*os.path.split(__file__)[:-1]))

from version import __version__
from secrets import API_KEY
from youtube_user import YTUser, UsersDB
from constants import HEADERS_INSTRUCTIONS, ID_INSTRUCTIONS


USERS: UsersDB = UsersDB()


# noinspection PyUnusedLocal
def handle_text(update: Update, context: CallbackContext) -> None:
    tg_id = update.message.chat_id
    user: YTUser = USERS[tg_id]
    txt = update.message.text
    reply = update.message.reply_to_message
    if reply and reply.text == HEADERS_INSTRUCTIONS.strip():
        user.store_headers(txt.strip())
        msg = "Youtube Music headers stored!"
    elif reply and reply.text == ID_INSTRUCTIONS.strip():
        user.yt_music_id = txt.strip()
        msg = "Youtube Music ID stored!"
    else:
        msg = "I don't understand :("

    update.message.reply_text(
        msg
    )

    return None


# noinspection PyUnusedLocal
def info(update: Update, context: CallbackContext) -> None:
    msg = "This is a bot for copying liked music playlist from Youtube music.\nVersion {}".format(
        __version__
    )
    update.message.reply_text(msg)
    return None


def error_handler(update: Update, context: CallbackContext) -> None:
    msg = f"An error occurred while handling that message:\n{context.error}"
    update.message.reply_text(msg)
    return None


# noinspection PyUnusedLocal
def register_headers(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        HEADERS_INSTRUCTIONS,
        reply_markup=ForceReply(),
    )
    return None


# noinspection PyUnusedLocal
def show_me(update: Update, context: CallbackContext) -> None:
    tg_id = update.message.chat_id
    user: YTUser = USERS[tg_id]
    msg = f"You are {user}"
    update.message.reply_text(
        msg,
    )
    return None


# noinspection PyUnusedLocal
def register_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        ID_INSTRUCTIONS,
        reply_markup=ForceReply(),

    )
    return None


# noinspection PyUnusedLocal
def copy_playlist(update: Update, context: CallbackContext) -> None:
    tg_id = update.message.chat_id
    user: YTUser = USERS[tg_id]
    res = user.copy_playlist()
    msg = f"Created playlist {res!r}"
    update.message.reply_text(
        msg,
    )
    return None


def main():
    updater = Updater(API_KEY, workers=1)

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    updater.dispatcher.add_handler(CommandHandler("register_headers", register_headers))
    updater.dispatcher.add_handler(CommandHandler("register_id", register_id))
    updater.dispatcher.add_handler(CommandHandler("copy_liked_music", copy_playlist))
    updater.dispatcher.add_handler(CommandHandler("show_me", show_me))
    updater.dispatcher.add_handler(CommandHandler("info", info))

    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
    return None


if __name__ == '__main__':
    main()
