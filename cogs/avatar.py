from revolt.ext import commands
import revolt

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar")
    async def avatar(self, ctx, user: revolt.User = None):
        # If no user is mentioned, use the message author
        user = user or ctx.author

        # Get avatar URL
        avatar_url = user.avatar.url if user.avatar else None

        if avatar_url:
            await ctx.send(
                embeds=[{
                    "title": f"{user.username}'s Avatar",
                    "image": {"url": avatar_url}
                }]
            )
        else:
            await ctx.send(f"{user.username} has no avatar.")

def setup(bot):
    bot.add_cog(Avatar(bot))
