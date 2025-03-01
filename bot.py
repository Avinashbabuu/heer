from pyrogram import Client, filters
import json
import os

# Cloned bots data file
CLONE_FILE = "cloned_bots.json"

# Function to check if bot token is valid
def check_bot_token(token):
    import requests
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url).json()
    return "ok" in response and response["ok"]

# Load cloned bots
def load_cloned_bots():
    if not os.path.exists(CLONE_FILE):
        return {"bots": []}
    with open(CLONE_FILE, "r") as file:
        return json.load(file)

# Save cloned bots
def save_cloned_bots(data):
    with open(CLONE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# /clone command
@Client.on_message(filters.command("clone"))
async def clone_bot(client, message):
    await message.reply("Send your bot token to clone your music bot.")

@Client.on_message(filters.private & filters.text)
async def handle_token(client, message):
    token = message.text.strip()
    
    # Validate bot token
    if not check_bot_token(token):
        await message.reply("Invalid bot token! Please try again.")
        return
    
    user_id = message.from_user.id
    cloned_bots = load_cloned_bots()

    # Check if already cloned
    for bot in cloned_bots["bots"]:
        if bot["token"] == token:
            await message.reply("This bot is already cloned.")
            return

    # Save cloned bot details
    bot_info = {"user_id": user_id, "token": token}
    cloned_bots["bots"].append(bot_info)
    save_cloned_bots(cloned_bots)

    await message.reply("✅ Your bot is being deployed! Please wait...")

    # Deploy bot using Termux (You can modify for VPS/Heroku)
    os.system(f"git clone https://github.com/Avinashbabuu/sara cloned_bot && cd cloned_bot && echo {token} > token.txt && bash start.sh")

    await message.reply("🎉 Your bot is successfully cloned and running!")
    
@Client.on_message(filters.command("delclone"))
async def del_clone(client, message):
    token = message.text.split(" ", 1)[1].strip()
    cloned_bots = load_cloned_bots()
    
    # Find & remove bot
    updated_bots = [bot for bot in cloned_bots["bots"] if bot["token"] != token]
    
    if len(updated_bots) == len(cloned_bots["bots"]):
        await message.reply("❌ This bot is not found in our records.")
        return

    # Save updated data
    cloned_bots["bots"] = updated_bots
    save_cloned_bots(cloned_bots)

    os.system(f"rm -rf cloned_bot")  # Remove cloned bot directory

    await message.reply("✅ Your cloned bot has been removed successfully.")
    
@Client.on_message(filters.command("manageclones"))
async def manage_clones(client, message):
    cloned_bots = load_cloned_bots()
    
    if not cloned_bots["bots"]:
        await message.reply("No cloned bots found.")
        return

    bot_list = "\n".join([f"👤 User ID: {bot['user_id']} | Token: {bot['token']}" for bot in cloned_bots["bots"]])
    await message.reply(f"🔹 Cloned Bots List:\n\n{bot_list}")

@Client.on_message(filters.command("removeclone"))
async def remove_clone(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Usage: /removeclone <bot_token>")
        return
    
    token = message.command[1]
    cloned_bots = load_cloned_bots()
    
    # Check if bot exists
    updated_bots = [bot for bot in cloned_bots["bots"] if bot["token"] != token]
    
    if len(updated_bots) == len(cloned_bots["bots"]):
        await message.reply("❌ This bot is not found in our records.")
        return

    # Save updated data
    cloned_bots["bots"] = updated_bots
    save_cloned_bots(cloned_bots)

    os.system(f"rm -rf cloned_bot")  # Remove cloned bot directory

    await message.reply("✅ Cloned bot has been removed successfully.")

@Client.on_message(filters.command("cast"))
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
            os.system(f"python3 cloned_bot.py --message '{text}' --token {bot['token']}")
            success += 1
        except:
            failed += 1

    await message.reply(f"✅ Broadcast completed!\nSuccess: {success}\nFailed: {failed}")
