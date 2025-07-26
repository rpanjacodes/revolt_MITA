from revolt.ext import commands
import time

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        # Measure latency (message round-trip)
        start = time.perf_counter()
        msg = await ctx.send("Pinging...")
        end = time.perf_counter()
        latency_ms = (end - start) * 1000

        # WebSocket latency
        ws_latency_ms = self.bot.latency * 1000  # Convert to ms

        # Edit the message with results
        await msg.edit(content=(
            f"🏓 Pong!\n"
            f"• Latency: `{latency_ms:.2f} ms`\n"
            f"• WebSocket: `{ws_latency_ms:.2f} ms`"
        ))

def setup(bot):
    bot.add_cog(Ping(bot))
