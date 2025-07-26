from revolt.ext import commands
from db import Database
import asyncio
import aiohttp
import os

class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

        # Set your API Key and model here, or use env variables
        self.shapesinc_api_key = os.getenv("SHAPESINC_API_KEY", "your-api-key-here")
        self.shapesinc_model = os.getenv("SHAPESINC_MODEL", "shapesinc/hera-7b-dpo")

    async def shapesinc_response(self, prompt):
        url = "https://api.shapesinc.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.shapesinc_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.shapesinc_model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"❌ Error: Shapesinc API returned {resp.status}"

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db.connect()
        await self.db.setup_tables()
        print("✅ ChatBot DB connected and ready.")

    @commands.command(name="setchat")
    async def set_chat_channel(self, ctx):
        server_id = str(ctx.server.id)
        channel_id = str(ctx.channel.id)

        await self.db.set_chatbot_channel(server_id, channel_id)
        await ctx.send("✅ This channel is now the chatbot channel.")

    @commands.command(name="removechat")
    async def remove_chat_channel(self, ctx):
        server_id = str(ctx.server.id)

        await self.db.remove_chatbot_channel(server_id)
        await ctx.send("❌ Chatbot channel removed. I will no longer reply in any channel.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.server:
            return

        server_id = str(message.server.id)
        channel_id = str(message.channel.id)
        chatbot_channel = await self.db.get_chatbot_channel(server_id)

        if chatbot_channel == channel_id:
            prompt = message.content
            reply = await self.shapesinc_response(prompt)
            await message.channel.send(reply)

def setup(bot):
    bot.add_cog(ChatBot(bot))
