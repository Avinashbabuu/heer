import telebot
import requests
import os
import json

TOKEN = "8024398292:AAF8X8PF4Z-2hDSBkiQMOzSWD2FA8kQLZ1g"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID
cloned_bots_file = "cloned_bots.json"

# Load cloned bots data
def load_cloned_bots():
    if not os.path.exists(cloned_bots_file):
        return {}
    with open(cloned_bots_file, "r") as f:
        return json.load(f)

# Save cloned bots data
def save_cloned_bots(data):
    with open(cloned_bots_file, "w") as f:
        json.dump(data, f, indent=4)

cloned_bots = load_cloned_bots()

# Clone bot function
@bot.message_handler(commands=['clone'])
def clone_bot(message):
    bot.send_message(message.chat.id, "Send me your bot token from BotFather:")
    bot.register_next_step_handler(message, process_bot_clone)

def process_bot_clone(message):
    user_id = message.chat.id
    new_token = message.text.strip()
    
    # Verify bot token
    response = requests.get(f"https://api.telegram.org/bot{new_token}/getMe").json()
    
    if not response.get("ok"):
        bot.send_message(user_id, "❌ Invalid bot token! Please try again.")
        return
    
    new_bot_username = response["result"]["username"]
    
    # Save bot details
    cloned_bots[new_bot_username] = {
        "user_id": user_id,
        "bot_token": new_token,
        "groups": []
    }
    save_cloned_bots(cloned_bots)
    
    bot.send_message(user_id, f"✅ Successfully cloned `{new_bot_username}`!\n\nNow, deploy it using the same GitHub repository.", parse_mode="Markdown")

# Show user's cloned bots
@bot.message_handler(commands=['myclones'])
def my_cloned_bots(message):
    user_id = message.chat.id
    user_bots = [bot for bot, data in cloned_bots.items() if data["user_id"] == user_id]

    if not user_bots:
        bot.send_message(user_id, "❌ You haven't cloned any bots yet.")
        return

    bot_list = "\n".join([f"@{b}" for b in user_bots])
    bot.send_message(user_id, f"✅ Your cloned bots:\n{bot_list}")

# Remove own cloned bot
@bot.message_handler(commands=['delclone'])
def remove_clone_user(message):
    user_id = message.chat.id
    args = message.text.split(" ")
    
    if len(args) < 2:
        bot.send_message(user_id, "❌ Usage: `/delclone <bot_token>`", parse_mode="Markdown")
        return
    
    bot_token = args[1].strip()
    
    for bot_username, data in cloned_bots.items():
        if data["user_id"] == user_id and data["bot_token"] == bot_token:
            del cloned_bots[bot_username]
            save_cloned_bots(cloned_bots)
            bot.send_message(user_id, f"✅ `{bot_username}` has been removed!", parse_mode="Markdown")
            return
    
    bot.send_message(user_id, "❌ You don't own this bot or invalid token.", parse_mode="Markdown")

# Admin manage cloned bots
@bot.message_handler(commands=['manageclones'])
def manage_cloned_bots(message):
    if message.chat.id != admin_id:
        bot.send_message(message.chat.id, "❌ You are not authorized.")
        return

    if not cloned_bots:
        bot.send_message(admin_id, "❌ No cloned bots found.")
        return

    bot_list = "\n".join([f"@{b} - User: {data['user_id']}" for b, data in cloned_bots.items()])
    bot.send_message(admin_id, f"🔹 **Cloned Bots:**\n{bot_list}", parse_mode="Markdown")

# Remove a cloned bot (Admin Only)
@bot.message_handler(commands=['removeclone'])
def remove_clone_admin(message):
    if message.chat.id != admin_id:
        bot.send_message(message.chat.id, "❌ You are not authorized.")
        return

    args = message.text.split(" ")
    if len(args) < 2:
        bot.send_message(admin_id, "❌ Usage: `/removeclone @BotUsername`", parse_mode="Markdown")
        return

    bot_username = args[1].replace("@", "")

    if bot_username in cloned_bots:
        del cloned_bots[bot_username]
        save_cloned_bots(cloned_bots)
        bot.send_message(admin_id, f"✅ `{bot_username}` has been removed!", parse_mode="Markdown")
    else:
        bot.send_message(admin_id, "❌ Bot not found in cloned list.", parse_mode="Markdown")

# Broadcast to all cloned bots in groups
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.chat.id != admin_id:
        bot.send_message(message.chat.id, "❌ You are not authorized.")
        return

    text = message.text.replace("/broadcast", "").strip()
    if not text:
        bot.send_message(admin_id, "❌ Usage: `/broadcast Your Message`", parse_mode="Markdown")
        return

    for bot_username, data in cloned_bots.items():
        bot_token = data["bot_token"]
        
        # Get all groups the bot is in
        try:
            updates = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates").json()
            group_ids = set()
            for update in updates.get("result", []):
                if "message" in update and "chat" in update["message"] and update["message"]["chat"]["type"] in ["group", "supergroup"]:
                    group_ids.add(update["message"]["chat"]["id"])

            # Send the broadcast message to all groups
            for group_id in group_ids:
                requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                             params={"chat_id": group_id, "text": text})
                
        except:
            pass  # Ignore if bot is down

    bot.send_message(admin_id, "✅ Broadcast sent to all cloned bots in groups!")

bot.polling(none_stop=True)
