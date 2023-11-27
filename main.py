from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from shayari import shayari_list
from jokes import jokes_list
from songs import songs_lyrics
from love import love_shayari
from dialogues import dialogue_list
import random
import os

# Dictionary to store approved users in groups
approved_users = {}

def format_message(content: str, category: str) -> str:
    return f"🌟 *{category}*: {content} 🌟"

def is_group_admin(update: Update) -> bool:
    user_id = update.effective_user.id
    return update.effective_chat.get_member(user_id).status in ['administrator', 'creator']

def process_command(update: Update, context: CallbackContext, content_list: list, category: str) -> None:
    user_id = update.effective_user.id

    if user_id in approved_users.get(update.effective_chat.id, []) or is_group_admin(update):
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
    else:
        update.message.reply_text("Only approved users and group administrators can use this command here. You can use it in private message mode or ask admins to approve you by using /sapprove command")

def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        # Handle start command in private messages differently
        update.message.reply_text("Welcome! You can use commands like /sspam, /joke, /gana, /mspam and /dialogue.")
    else:
        # Check if the user is a group administrator
        if not is_group_admin(update):
            update.message.reply_text("Only group administrators can start the bot in this group.")
            return

        # Bot logic for group start command
        # ...

def sspam(update: Update, context: CallbackContext) -> None:
    process_command(update, context, shayari_list, "Shayari")

def joke(update: Update, context: CallbackContext) -> None:
    process_command(update, context, jokes_list, "Joke")

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
    process_command(update, context, love_shayari, "Love Shayari")

def dialogue(update: Update, context: CallbackContext) -> None:
    process_command(update, context, dialogue_list, "Dialogue")

def sstop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🛑 Spamming process stopped. Type /sspam for Shayari, /joke for jokes, /gana for song lyrics, /mspam for love Shayari, /dialogue for dialogues. 🛑", parse_mode=ParseMode.MARKDOWN)

def sapprove_command(update: Update, context: CallbackContext) -> None:
    approving_admin = update.effective_user
    user_to_approve = context.args[0] if context.args else None

    # Check if the approving admin is a group administrator
    if not is_group_admin(update):
        update.message.reply_text("Only group administrators can approve users.")
        return

    if user_to_approve:
        # Process approval logic and update approved_users dictionary
        group_id = update.effective_chat.id
        approved_users.setdefault(group_id, set()).add(user_to_approve)
        update.message.reply_text(f"User {user_to_approve} has been approved for command usage.")
    else:
        update.message.reply_text("Please provide a user ID or username to approve.")

def main() -> None:
    updater = Updater(os.environ.get("BOT_TOKEN"))  # BOT_TOKEN is set in the Heroku Config Vars

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sspam", sspam, pass_args=True))
    dp.add_handler(CommandHandler("joke", joke, pass_args=True))
    dp.add_handler(CommandHandler("gana", gana, pass_args=True))
    dp.add_handler(CommandHandler("mspam", mspam, pass_args=True))
    dp.add_handler(CommandHandler("dialogue", dialogue, pass_args=True))
    dp.add_handler(CommandHandler("dialogues", dialogue, pass_args=True))
    dp.add_handler(CommandHandler("sstop", sstop))
    dp.add_handler(CommandHandler("sapprove", sapprove_command, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
