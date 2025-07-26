import revolt
from revolt.ext import commands
import os
import asyncio

# Set your bot token here
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Create the bot instance with prefix "!"
intents = revolt.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# On bot ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    # Load all cogs from "cogs" folder
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

# Start the bot
async def start():
    await bot.start(BOT_TOKEN)

# Run the bot with asyncio
if __name__ == "__main__":
    asyncio.run(start())
