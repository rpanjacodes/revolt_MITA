from revolt.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    async def say(self, ctx, *, content: str):
        # Split message into text + image URL
        parts = content.rsplit(" ", 1)

        if len(parts) != 2:
            await ctx.send("❌ Usage: `!say <message> <image_url>`")
            return

        text, image_url = parts

        # Check if URL ends with image extension
        if not image_url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            await ctx.send("❌ Invalid image URL. Must end with `.png`, `.jpg`, `.jpeg`, `.gif`, or `.webp`.")
            return

        # Send embed with text and image
        await ctx.send(
            content=text,
            embeds=[{
                "image": {"url": image_url}
            }]
        )

def setup(bot):
    bot.add_cog(Say(bot))
