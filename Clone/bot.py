import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Aapke bot ka main token
TOKEN = "8024398292:AAFHzwE4ICoAba0S7DsSaDk5nykSJHP3sQE"
GITHUB_REPO = "https://github.com/Avinashbabuu/sara.git"

app = Application.builder().token(TOKEN).build()

async def clone(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text("⚠️ *Usage:* `/clone YOUR_BOT_TOKEN`")
        return
    
    new_bot_token = context.args[0]
    user_id = update.effective_user.id  # Clone karne wale user ka Telegram ID
    
    bot_folder = f"/root/cloned_bots/{user_id}"
    
    if not os.path.exists(bot_folder):
        os.makedirs(bot_folder)

    await update.message.reply_text("🔄 Cloning your bot.....")

    # GitHub se repo clone karo
    subprocess.run(["git", "clone", GITHUB_REPO, bot_folder], check=True)

    # `.env` file create karo aur details save karo
    env_content = f"""API_ID=22748653
API_HASH=29bba513726e776d0b5fd55dfa893c5a
BOT_TOKEN={new_bot_token}
OWNER_ID={user_id}
STRING_SESSION=BQFbHe0AgLJG08--K2ymLyU5rNb89fDVrpDj4Y0ynqEF4BeUUUS3DmDZFmH_JbW596B3mfCUtF6bqu7M1ALkAZnP0dPg160t7WCkYdxqS7jVNEnuOiZgJSTbjNbhQoN8HgRHQK_pt7B42Z802uHWMC7bz0PRZOMHwNu16oDldgZolWueouHhVitQr0zAV9EctiR_PCZJwxXdxZjVgP0MeY3lVJr5XnfUcgKxXAqCx6_HfTUNfiT7xJ3rO2J5sdQSSrnzuJkfM9U2KVOw2pGx30IJqslmBPUHmhCUwSpp86rGP7S8KDFcMjGN-zUYgCVbded0sRzY13p6SAcMwRXN8Wn5EtmS1gAAAAHdyX_DAA
MONGO_DB_URI=mongodb+srv://Avinash12:Avinash123@cluster0.5y3t1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
SUPPORT_CHANNEL=https://t.me/Nepsxbot
SUPPORT_CHAT=https://t.me/Friend_Forever_Groups
START_IMG_URL=https://files.catbox.moe/rca1m3.jpg
PING_IMG_URL=https://files.catbox.moe/9cevdg.jpg
"""

    with open(f"{bot_folder}/.env", "w") as f:
        f.write(env_content)

    await update.message.reply_text("✅ Repository cloned successfully!")

    # Install dependencies
    subprocess.run(["pip", "install", "-r", f"{bot_folder}/requirements.txt"], check=True)

    await update.message.reply_text("📦 Dependencies installed!")

    # Bot start karo
    subprocess.run(["python3", f"{bot_folder}/bot.py"], check=True)

    await update.message.reply_text(f"🎉 Your bot is now live!\n🆔 Owner ID: `{user_id}`")

app.add_handler(CommandHandler("clone", clone))

app.run_polling()
