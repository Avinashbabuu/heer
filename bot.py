from telebot import TeleBot
import os
import time

TOKEN = "8024398292:AAEAWFrPxYcdVoDUEztuObxBr7CH5m5lwgs"
bot = TeleBot(TOKEN)

# ✅ Sirf /clone command par response dega
@bot.message_handler(commands=['clone'])
def clone_bot(message):
    bot.send_message(message.chat.id, "🤖 *Bot Cloning Process Started...* \n\n🔍 Fetching bot details...", parse_mode="Markdown")
    
    time.sleep(2)
    bot.send_chat_action(message.chat.id, 'typing')  # Typing animation

    msg = bot.send_message(message.chat.id, "📝 *Enter your bot token:*\n\n(Take token from [BotFather](https://t.me/BotFather))", parse_mode="Markdown", disable_web_page_preview=True)
    
    bot.register_next_step_handler(msg, process_clone)

# ✅ Token lene ke baad process karega
def process_clone(message):
    token = message.text.strip()
    
    if not token.startswith(""):
        bot.send_message(message.chat.id, "❌ *Invalid Bot Token! Please enter a correct token.*", parse_mode="Markdown")
        return

    bot.send_message(message.chat.id, "⏳ *Cloning bot... Please wait...*", parse_mode="Markdown")
    time.sleep(3)

    bot.send_chat_action(message.chat.id, 'typing')
    
    if os.path.exists("cloned_bot"):
        os.system("rm -rf cloned_bot")  # Pehle se cloned bot hai to delete karega

    os.system(f"git clone https://github.com/YOUR_REPO.git cloned_bot && cd cloned_bot && echo '{token}' > token.txt")

    bot.send_message(message.chat.id, f"✅ *Bot Cloned Successfully!*\n\n🤖 *Bot Name:* Cloned Bot\n📌 *Username:* @{message.from_user.username}\n\n🔥 *Your bot is now ready!*", parse_mode="Markdown")

# ✅ Agar user normal message bhejta hai to ignore karega
@bot.message_handler(func=lambda message: True)
def ignore_message(message):
    pass  # Kuch bhi reply nahi karega

bot.polling()

@bot.message_handler(commands=['delclone'])
def delete_clone(message):
    if os.path.exists("cloned_bot"):
        os.system("rm -rf cloned_bot")
        bot.send_message(message.chat.id, "✅ *Cloned Bot Deleted Successfully!*", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ *No Cloned Bot Found!*", parse_mode="Markdown")

bot.polling()
