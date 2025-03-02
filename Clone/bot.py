import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Cloned bots ka data store karne ke liye
CLONE_DIR = "/root/cloned_bots"  # VPS pe folder
os.makedirs(CLONE_DIR, exist_ok=True)

# `/clone` command function
def clone_bot(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /clone <bot_token>")
        return

    bot_token = context.args[0]

    # Bot token verify karna
    bot_info = subprocess.getoutput(f"curl -s https://api.telegram.org/bot{bot_token}/getMe")
    if '"ok":true' not in bot_info:
        update.message.reply_text("❌ Invalid bot token! Please check again.")
        return

    # Bot username nikalna
    bot_username = bot_info.split('"username":"')[1].split('"')[0]

    # Clone ka directory
    bot_path = os.path.join(CLONE_DIR, bot_username)

    if os.path.exists(bot_path):
        update.message.reply_text("⚠️ This bot is already cloned.")
        return

    os.makedirs(bot_path)

    # Repository clone karna
    update.message.reply_text(f"🚀 Cloning {bot_username} bot...")

    subprocess.run(f"git clone https://github.com/Avinashbabuu/sara {bot_path}", shell=True)

    # .env file set karna
    env_content = f"BOT_TOKEN={bot_token}\nDATABASE_URL=sqlite:///{bot_path}/database.db"
    with open(os.path.join(bot_path, ".env"), "w") as f:
        f.write(env_content)

    # Start karna cloned bot
    subprocess.run(f"cd {bot_path} && nohup python3 bot.py &", shell=True)

    update.message.reply_text(f"✅ {bot_username} successfully cloned and running!")

# `/remove_clone` command function
def remove_clone(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /remove_clone <bot_username>")
        return

    bot_username = context.args[0]
    bot_path = os.path.join(CLONE_DIR, bot_username)

    if not os.path.exists(bot_path):
        update.message.reply_text("❌ No such cloned bot found.")
        return

    subprocess.run(f"rm -rf {bot_path}", shell=True)
    update.message.reply_text(f"🗑️ {bot_username} has been removed.")

# Telegram bot setup
TOKEN = "8024398292:AAFHzwE4ICoAba0S7DsSaDk5nykSJHP3sQE"
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("clone", clone_bot, pass_args=True))
dp.add_handler(CommandHandler("remove_clone", remove_clone, pass_args=True))

updater.start_polling()
updater.idle()
