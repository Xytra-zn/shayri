from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from shayari import shayari_list
from jokes import jokes_list
from songs import songs_lyrics
from love import love_shayari
from dialogues import dialogue_list
import random
import os

def format_message(content: str, category: str) -> str:
    return f"🌟 *{category}*: {content} 🌟"

def process_command(update: Update, context: CallbackContext, content_list: list, category: str) -> None:
    args = context.args
    if not args:
        update.message.reply_text(f"Please use the command in the format `/{category} <number>`.")
        return

    try:
        num_items = int(args[0])
    except ValueError:
        update.message.reply_text("Please enter a valid number.")
        return

    if num_items <= 0:
        update.message.reply_text("Please enter a positive number.")
        return

    total_items = len(content_list)
    if num_items >= total_items:
        selected_items = content_list * (num_items // total_items) + random.sample(content_list, num_items % total_items)
    else:
        selected_items = random.sample(content_list, num_items)

    formatted_messages = [format_message(item, category) for item in selected_items]
    for formatted_message in formatted_messages:
        update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN)

def stop_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🛑 Process interrupted. 🛑", parse_mode=ParseMode.MARKDOWN)

def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        # Handle start command in private messages differently
        update.message.reply_text("Welcome! You can use commands like /sspam, /joke, /gana, /mspam, /dialogue, and /dialogues.")
    else:
        # Check if the user is a group administrator
        if not update.message.chat.get_member(update.message.from_user.id).status in ['administrator', 'creator']:
            update.message.reply_text("Only group administrators can start the bot in this group.")
            return

        # Bot logic for group start command
        # ...

def main() -> None:
    updater = Updater(os.environ.get("BOT_TOKEN"))  # BOT_TOKEN is set in the Heroku Config Vars

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sspam", process_command, pass_args=True, callback_args=[shayari_list, "Shayari"]))
    dp.add_handler(CommandHandler("joke", process_command, pass_args=True, callback_args=[jokes_list, "Joke"]))
    dp.add_handler(CommandHandler("gana", process_command, pass_args=True, callback_args=[songs_lyrics, "Song"]))
    dp.add_handler(CommandHandler("mspam", process_command, pass_args=True, callback_args=[love_shayari, "Love Shayari"]))
    dp.add_handler(CommandHandler("dialogue", process_command, pass_args=True, callback_args=[dialogue_list, "Dialogue"]))
    dp.add_handler(CommandHandler("dialogues", process_command, pass_args=True, callback_args=[dialogue_list, "Dialogue"]))
    dp.add_handler(CommandHandler("stop", stop_command))

    # Handle private messages to start the bot
    dp.add_handler(MessageHandler(Filters.chat_type.private & ~Filters.command, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
