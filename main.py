from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from shayari import shayari_list
from jokes import jokes_list
from songs import songs_lyrics
from love import love_shayari
from dialogues import dialogue_list
import random
import os
import threading

# Variable to keep track of the spamming process
spamming_process = None

def format_message(content: str, category: str) -> str:
    return f"🌟 *{category}*: {content} 🌟"

def spam_messages(update: Update, context: CallbackContext, content_list: list, category: str, num_messages: int) -> None:
    for _ in range(num_messages):
        selected_message = random.choice(content_list)
        formatted_message = format_message(selected_message, category)
        update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN)

def sspam(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("Please use the command in the format `/sspam <number>`.")
        return

    try:
        num_messages = int(args[0])
    except ValueError:
        update.message.reply_text("Please enter a valid number.")
        return

    if num_messages <= 0:
        update.message.reply_text("Please enter a positive number.")
        return

    global spamming_process
    if spamming_process and spamming_process.is_alive():
        update.message.reply_text("Spamming process is already running. Use `/sstop` to stop the current process.")
        return

    spamming_process = threading.Thread(target=spam_messages, args=(update, context, shayari_list, "Shayari", num_messages))
    spamming_process.start()

def stop_spamming(update: Update, context: CallbackContext) -> None:
    global spamming_process
    if spamming_process and spamming_process.is_alive():
        spamming_process.join()
        update.message.reply_text("🛑 Spamming process stopped. 🛑", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("No active spamming process.", parse_mode=ParseMode.MARKDOWN)

def joke(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("Please use the command in the format `/joke <number>`.")
        return

    num_jokes = 1
    try:
        num_jokes = int(args[0])
    except ValueError:
        update.message.reply_text("Please enter a valid number.")

    global spamming_process
    if spamming_process and spamming_process.is_alive():
        update.message.reply_text("Spamming process is already running. Use `/sstop` to stop the current process.")
        return

    spamming_process = threading.Thread(target=spam_messages, args=(update, context, jokes_list, "Joke", num_jokes))
    spamming_process.start()

def gana(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("Please provide a song name with the command. For example, `/gana song1`.")
        return

    song_name = args[0].lower()
    song_lyrics = songs_lyrics.get(song_name, "Lyrics not available for this song.")
    formatted_song = format_message(song_lyrics, "Song")
    update.message.reply_text(formatted_song, parse_mode=ParseMode.MARKDOWN)

def mspam(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("Please use the command in the format `/mspam <number>`.")
        return

    try:
        num_messages = int(args[0])
    except ValueError:
        update.message.reply_text("Please enter a valid number.")
        return

    if num_messages <= 0:
        update.message.reply_text("Please enter a positive number.")
        return

    global spamming_process
    if spamming_process and spamming_process.is_alive():
        update.message.reply_text("Spamming process is already running. Use `/sstop` to stop the current process.")
        return

    spamming_process = threading.Thread(target=spam_messages, args=(update, context, love_shayari, "Love Shayari", num_messages))
    spamming_process.start()

def dialogue(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("Please use the command in the format `/dialogue` or `/dialogues`.")
        return

    num_dialogues = 1
    try:
        num_dialogues = int(args[0])
    except ValueError:
        update.message.reply_text("Please enter a valid number.")

    global spamming_process
    if spamming_process and spamming_process.is_alive():
        update.message.reply_text("Spamming process is already running. Use `/sstop` to stop the current process.")
        return

    spamming_process = threading.Thread(target=spam_messages, args=(update, context, dialogue_list, "Dialogue", num_dialogues))
    spamming_process.start()

def main() -> None:
    updater = Updater(os.environ.get("BOT_TOKEN"))  # BOT_TOKEN is set in the Heroku Config Vars

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("sspam", sspam, pass_args=True))
    dp.add_handler(CommandHandler("joke", joke, pass_args=True))
    dp.add_handler(CommandHandler("gana", gana, pass_args=True))
    dp.add_handler(CommandHandler("mspam", mspam, pass_args=True))
    dp.add_handler(CommandHandler("dialogue", dialogue, pass_args=True))
    dp.add_handler(CommandHandler("dialogues", dialogue, pass_args=True))
    dp.add_handler(CommandHandler("sstop", stop_spamming))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
