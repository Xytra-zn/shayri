from telegram import Update, ParseMode, InputUser
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from shayari import shayari_list
from jokes import jokes_list
from songs import songs_lyrics
from love import love_shayari
from dialogues import dialogue_list
import random
import os

approved_users = {}

def format_message(content: str, category: str) -> str:
    return f"🌟 *{category}*: {content} 🌟"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Shayari Bot! Type /gpthelp to see all available commands.")

def is_group_admin(update: Update) -> bool:
    # Check if the user sending the message is a group admin
    user = update.effective_user
    chat = update.effective_chat
    return chat.get_member(user.id).status in ('administrator', 'creator')

def sspam(update: Update, context: CallbackContext) -> None:
    # Your existing sspam code

def joke(update: Update, context: CallbackContext) -> None:
    # Your existing joke code

def gana(update: Update, context: CallbackContext) -> None:
    # Modify the gana command to use the song name
    args = context.args
    if not args:
        update.message.reply_text("Please provide a song name with the command. For example, `/gana song1`.")
        return

    song_name = args[0].lower()
    song_lyrics = songs_lyrics.get(song_name, "Lyrics not available for this song.")
    formatted_song = format_message(song_lyrics, "Song")
    update.message.reply_text(formatted_song, parse_mode=ParseMode.MARKDOWN)

def mspam(update: Update, context: CallbackContext) -> None:
    # Your existing mspam code

def dialogue(update: Update, context: CallbackContext) -> None:
    # Your existing dialogue code

def sstop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🛑 Spamming process stopped. Type /sspam for Shayari, /joke for jokes, /gana for song lyrics, /mspam for love Shayari, /dialogue for dialogues. 🛑", parse_mode=ParseMode.MARKDOWN)

def permit(update: Update, context: CallbackContext) -> None:
    # Your existing sapprove command code with modifications
    approving_admin = update.effective_user
    user_to_approve = context.args[0] if context.args else None

    # Check if the approving admin is a group administrator
    if not is_group_admin(update):
        update.message.reply_text("Only group administrators can approve users.")
        return

    if user_to_approve:
        group_id = update.effective_chat.id

        if user_to_approve not in approved_users.get(group_id, []):
            # Call the Telegram API to get user information
            user_info = context.bot.get_chat_member(group_id, user_to_approve)
            user_id = user_info.user.id
            username = user_info.user.username

            # Add the user to the approved list
            approved_users.setdefault(group_id, []).append(user_id)

            update.message.reply_text(f"User {username} has been approved to use the commands.")
        else:
            update.message.reply_text("This user is already approved.")
    else:
        update.message.reply_text("Please provide a username or user ID to approve.")

def rmpermit(update: Update, context: CallbackContext) -> None:
    # Your existing sunapprove command code with modifications
    approving_admin = update.effective_user
    user_to_unapprove = context.args[0] if context.args else None

    # Check if the approving admin is a group administrator
    if not is_group_admin(update):
        update.message.reply_text("Only group administrators can unapprove users.")
        return

    if user_to_unapprove:
        group_id = update.effective_chat.id

        if user_to_unapprove in approved_users.get(group_id, []):
            # Remove the user from the approved list
            approved_users[group_id].remove(user_to_unapprove)

            update.message.reply_text("User has been unapproved.")
        else:
            update.message.reply_text("This user is not approved.")
    else:
        update.message.reply_text("Please provide a username or user ID to unapprove.")

def gpthelp(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Here are the available commands:\n"
                              "/gptstart - Start the bot\n"
                              "/sspam <number> - Get Shayari\n"
                              "/joke <number> - Get Jokes\n"
                              "/gana <song_name> - Get Song Lyrics\n"
                              "/mspam <number> - Get Love Shayari\n"
                              "/dialogue <number> - Get Dialogues\n"
                              "/sstop - Stop spamming process\n"
                              "/permit <username or user ID> - Approve a user to use commands\n"
                              "/rmpermit <username or user ID> - Unapprove a user\n"
                              "/gpthelp - Show this help message")

def main() -> None:
    updater = Updater(os.environ.get("BOT_TOKEN"))  # BOT_TOKEN is set in the Heroku Config Vars

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("gptstart", start))
    dp.add_handler(CommandHandler("sspam", sspam, pass_args=True))
    dp.add_handler(CommandHandler("joke", joke, pass_args=True))
    dp.add_handler(CommandHandler("gana", gana, pass_args=True))
    dp.add_handler(CommandHandler("mspam", mspam, pass_args=True))
    dp.add_handler(CommandHandler("dialogue", dialogue, pass_args=True))
    dp.add_handler(CommandHandler("sstop", sstop))
    dp.add_handler(CommandHandler("permit", permit, pass_args=True))
    dp.add_handler(CommandHandler("rmpermit", rmpermit, pass_args=True))
    dp.add_handler(CommandHandler("gpthelp", gpthelp))

    # Handle private messages to start the bot
    dp.add_handler(MessageHandler(Filters.private & ~Filters.command, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
