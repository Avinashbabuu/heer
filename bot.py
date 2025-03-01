import os
import telebot

TOKEN = "8024398292:AAF8X8PF4Z-2hDSBkiQMOzSWD2FA8kQLZ1g"  # Apne bot ka token yaha dal do
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['clone'])
def get_token(message):
    bot.send_message(message.chat.id, "Send me your new bot's Token.")
    bot.register_next_step_handler(message, deploy_clone)

def deploy_clone(message):
    new_token = message.text.strip()
    user_id = message.chat.id

    if not new_token.startswith("8"):  # Token ka format check karne ke liye
        bot.send_message(user_id, "❌ Invalid bot token! Please send a correct one.")
        return

    # Clone ka script
    clone_script = f"""
    #!/bin/bash
    rm -rf cloned_bot
    git clone https://github.com/Avinashbabuu/sara cloned_bot
    cd cloned_bot
    echo 'TOKEN = "{new_token}"' > config.py
    pip install -r requirements.txt
    nohup python3 bot.py &
    echo "✅ Bot Cloned Successfully!"
    """

    script_path = f"/tmp/clone_{user_id}.sh"
    with open(script_path, "w") as script:
        script.write(clone_script)

    bot.send_message(user_id, "⏳ Cloning your bot... Please wait.")

    os.system(f"chmod +x {script_path} && bash {script_path}")
    bot.send_message(user_id, "✅ Bot Cloned! Check if it's running.")

    cloned_bots = {}

@bot.message_handler(commands=['mybots'])
def list_cloned_bots(message):
    user_id = message.chat.id
    if user_id not in cloned_bots:
        bot.send_message(user_id, "🚫 You haven't cloned any bots yet.")
    else:
        bots_list = "\n".join(cloned_bots[user_id])
        bot.send_message(user_id, f"🤖 Your cloned bots:\n{bots_list}")

    
bot.polling()
