import os
import git
import telebot
import subprocess

TOKEN = "8024398292:AAEAWFrPxYcdVoDUEztuObxBr7CH5m5lwgs"  # Apne bot ka token yaha daalo
bot = telebot.TeleBot(TOKEN)

# Clone command
@bot.message_handler(commands=['clone'])
def clone_bot(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Send your BotFather bot token to clone your bot.")

    @bot.message_handler(func=lambda msg: True)
    def get_token(msg):
        user_token = msg.text
        user_id = msg.from_user.id
        repo_url = "https://github.com/Avinashbabuu/sara.git"
        user_folder = f"cloned_bots/bot_{user_id}"

        if os.path.exists(user_folder):
            bot.send_message(chat_id, "Your bot is already cloned!")
            return

        try:
            bot.send_message(chat_id, "Cloning your bot... Please wait ⏳")
            git.Repo.clone_from(repo_url, user_folder)
            
            # Updating token
            config_path = os.path.join(user_folder, "config.py")
            with open(config_path, "w") as config_file:
                config_file.write(f'BOT_TOKEN = "{user_token}"\n')

            # Installing requirements
            subprocess.run(["pip", "install", "-r", os.path.join(user_folder, "requirements.txt")])

            # Running bot
            subprocess.Popen(["python3", os.path.join(user_folder, "bot.py")])

            bot.send_message(chat_id, f"✅ Your bot is cloned successfully!\n\n🔗 Username: @{message.chat.username}")
        
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")

bot.polling()
