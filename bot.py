import os
import json
import requests
from pyrogram import Client, filters

API_ID = 22748653  # 🔹 Your API ID from my.telegram.org
API_HASH = "29bba513726e776d0b5fd55dfa893c5a"  # 🔹 Your API Hash from my.telegram.org
BOT_TOKEN = "8024398292:AAF8X8PF4Z-2hDSBkiQMOzSWD2FA8kQLZ1g"  # 🔹 Your main bot token

# 🔹 Cloned bots storage file
CLONE_FILE = "cloned_bots.json"

# 🔹 Initialize the bot
app = Client("MainCloneBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔹 Function to check bot token validity
def check_bot_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url).json()
    return response.get("ok", False)

# 🔹 Load cloned bots
def load_cloned_bots():
    if not os.path.exists(CLONE_FILE):
        return {"bots": []}
    with open(CLONE_FILE, "r") as file:
        return json.load(file)

# 🔹 Save cloned bots
def save_cloned_bots(data):
    with open(CLONE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# 📌 **/clone Command**
@app.on_message(filters.command("clone") & filters.private)
async def clone_bot(client, message):
    await message.reply("🔹 Send your bot token to clone your music bot.")

@app.on_message(filters.private & filters.text)
async def handle_token(client, message):
    token = message.text.strip()

    # 🔹 Validate token
    if not check_bot_token(token):
        await message.reply("❌ Invalid bot token! Please try again.")
        return

    user_id = message.from_user.id
    cloned_bots = load_cloned_bots()

    # 🔹 Check if already cloned
    for bot in cloned_bots["bots"]:
        if bot["token"] == token:
            await message.reply("✅ This bot is already cloned.")
            return

    # 🔹 Save cloned bot details
    bot_info = {"user_id": user_id, "token": token}
    cloned_bots["bots"].append(bot_info)
    save_cloned_bots(cloned_bots)

    await message.reply("🚀 Deploying your bot... Please wait!")

    # 🔹 Deploy bot (Change this if running on VPS)
    os.system(f"git clone https://github.com/Avinashbabuu/sara cloned_bot && cd cloned_bot && echo {token} > token.txt && bash start.sh")

    await message.reply("🎉 Your bot has been cloned and is running!")

# 📌 **/delclone Command (User Can Remove Own Clone)**
@app.on_message(filters.command("delclone") & filters.private)
async def del_clone(client, message):
    user_id = message.from_user.id
    cloned_bots = load_cloned_bots()

    updated_bots = [bot for bot in cloned_bots["bots"] if bot["user_id"] != user_id]
    
    if len(updated_bots) == len(cloned_bots["bots"]):
        await message.reply("❌ You don't have any cloned bot.")
        return

    # 🔹 Save updated list
    cloned_bots["bots"] = updated_bots
    save_cloned_bots(cloned_bots)

    os.system(f"rm -rf cloned_bot")  # Remove bot directory

    await message.reply("✅ Your cloned bot has been removed successfully.")

# 📌 **/manageclones Command (Admin View)**
@app.on_message(filters.command("manageclones") & filters.private)
async def manage_clones(client, message):
    cloned_bots = load_cloned_bots()
    
    if not cloned_bots["bots"]:
        await message.reply("❌ No cloned bots found.")
        return

    bot_list = "\n".join([f"👤 User ID: {bot['user_id']} | Token: {bot['token']}" for bot in cloned_bots["bots"]])
    await message.reply(f"🔹 Cloned Bots List:\n\n{bot_list}")

# 📌 **/removeclone Command (Admin Remove Specific Clone)**
@app.on_message(filters.command("removeclone") & filters.private)
async def remove_clone(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Usage: /removeclone <bot_token>")
        return
    
    token = message.command[1]
    cloned_bots = load_cloned_bots()

    updated_bots = [bot for bot in cloned_bots["bots"] if bot["token"] != token]

    if len(updated_bots) == len(cloned_bots["bots"]):
        await message.reply("❌ Bot not found in records.")
        return

    # 🔹 Save updated list
    cloned_bots["bots"] = updated_bots
    save_cloned_bots(cloned_bots)

    os.system(f"rm -rf cloned_bot")  # Remove bot directory

    await message.reply("✅ Cloned bot has been removed.")

# 📌 **/cast Command (Broadcast to All Cloned Bots)**
@app.on_message(filters.command("cast") & filters.private)
async def broadcast_message(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Usage: /cast <message>")
        return

    text = " ".join(message.command[1:])
    cloned_bots = load_cloned_bots()

    if not cloned_bots["bots"]:
        await message.reply("❌ No cloned bots found.")
        return

    success, failed = 0, 0
    for bot in cloned_bots["bots"]:
        try:
            url = f"https://api.telegram.org/bot{bot['token']}/sendMessage"
            requests.post(url, json={"chat_id": bot["user_id"], "text": text})
            success += 1
        except:
            failed += 1

    await message.reply(f"✅ Broadcast completed!\nSuccess: {success}\nFailed: {failed}")

# 🔹 Run the bot
app.run()
