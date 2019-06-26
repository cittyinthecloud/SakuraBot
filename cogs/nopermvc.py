import discord
from discord.ext import commands
from utils.database import get_guild_settings


class NoPermVCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, _: discord.Member, after: discord.Member):

        settings = await get_guild_settings(after.guild)

        if settings.kick_on_losing_connect_perms and after.voice is not None and after.voice.channel is not None:
            permissions = after.voice.channel.permissions_for(after)
            if not permissions.connect:
                return await after.move_to(None)


def setup(bot):
    bot.add_cog(NoPermVCCog(bot))
