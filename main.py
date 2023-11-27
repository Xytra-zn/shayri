from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from shayari import shayari_list
from jokes import jokes_list
from songs import songs_lyrics
from love import love_shayari
from dialogues import dialogue_list
import random
import os

MAX_MESSAGES = 5

def format_message(content: str, category: str) -> str:
    return f"🌟 *{category}*: {content} 🌟"

def send_messages(update: Update, context: CallbackContext, content_list: list, category: str, num_messages: int = 1) -> None:
    num_messages = min(num_messages, MAX_MESSAGES)
    selected_messages = random.sample(content_list, num_messages)

    formatted_messages = [format_message(message, category) for message in selected_messages]
    for formatted_message in formatted_messages:
        update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN)

def sspam(update: Update, context: CallbackContext) -> None:
    args = context.args
    num_messages = int(args[0]) if args and args[0].isdigit() else 1
    send_messages(update, context, shayari_list, "Shayari", num_messages)

def joke(update: Update, context: CallbackContext) -> None:
    args = context.args
    num_messages = int(args[0]) if args and args[0].isdigit() else 1
    send_messages(update, context, jokes_list, "Joke", num_messages)

def gana(update: Update, context: CallbackContext) -> None:
    args = context.args
    song_name = args[0].lower() if args else None
    song_lyrics = songs_lyrics.get(song_name, "Lyrics not available for this song.")
    formatted_song = format_message(song_lyrics, "Song")
    update.message.reply_text(formatted_song, parse_mode=ParseMode.MARKDOWN)

def mspam(update: Update, context: CallbackContext) -> None:
    args = context.args
    num_messages = int(args[0]) if args and args[0].isdigit() else 1
    send_messages(update, context, love_shayari, "Love Shayari", num_messages)

def dialogue(update: Update, context: CallbackContext) -> None:
    args = context.args
    num_messages = int(args[0]) if args and args[0].isdigit() else 1
    send_messages(update, context, dialogue_list, "Dialogue", num_messages)

def main() -> None:
    updater = Updater(os.environ.get("BOT_TOKEN"))  # BOT_TOKEN is set in the Heroku Config Vars

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("sspam", sspam, pass_args=True))
    dp.add_handler(CommandHandler("joke", joke, pass_args=True))
    dp.add_handler(CommandHandler("gana", gana, pass_args=True))
    dp.add_handler(CommandHandler("mspam", mspam, pass_args=True))
    dp.add_handler(CommandHandler("dialogue", dialogue, pass_args=True))
    dp.add_handler(CommandHandler("dialogues", dialogue, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
