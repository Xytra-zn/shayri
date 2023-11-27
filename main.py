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

def process_command(update: Update, context: CallbackContext) -> None:
    command_args = context.args
    if not command_args:
        update.message.reply_text("Please provide the command in the format `/<category> <number>`.")
        return

    category = command_args[0].lower()
    content_list = None

    if category == 'sspam':
        content_list = shayari_list
    elif category == 'joke':
        content_list = jokes_list
    elif category == 'gana':
        content_list = songs_lyrics
    elif category == 'mspam':
        content_list = love_shayari
    elif category in ['dialogue', 'dialogues']:
        content_list = dialogue_list

    if content_list:
        process_command_for_category(update, context, content_list, category)
    else:
        update.message.reply_text("Invalid category. Supported categories are: sspam, joke, gana, mspam, dialogue(s).")

def process_command_for_category(update: Update, context: CallbackContext, content_list: list, category: str) -> None:
    command_args = context.args[1:]  # Exclude the category from the arguments
    try:
        num_items = int(command_args[0])
    except (ValueError, IndexError):
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

    formatted_messages = [format_message(item, category.capitalize()) for item in selected_items]
    for formatted_message in formatted_messages:
        update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN)

def stop_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🛑 Process interrupted. 🛑", parse_mode=ParseMode.MARKDOWN)

def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        update.message.reply_text("Welcome! You can use commands like /sspam, /joke, /gana, /mspam, /dialogue, and /dialogues.")
    else:
        if not update.message.chat.get_member(update.message.from_user.id).status in ['administrator', 'creator']:
            update.message.reply_text("Only group administrators can start the bot in this group.")
            return

def main() -> None:
    updater = Updater(os.environ.get("BOT_TOKEN"))

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sspam", process_command, pass_args=True))
    dp.add_handler(CommandHandler("joke", process_command, pass_args=True))
    dp.add_handler(CommandHandler("gana", process_command, pass_args=True))
    dp.add_handler(CommandHandler("mspam", process_command, pass_args=True))
    dp.add_handler(CommandHandler("dialogue", process_command, pass_args=True))
    dp.add_handler(CommandHandler("dialogues", process_command, pass_args=True))
    dp.add_handler(CommandHandler("stop", stop_command))

    dp.add_handler(MessageHandler(Filters.chat_type.private & ~Filters.command, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
