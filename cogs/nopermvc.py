import discord
from discord.ext import commands
from utils.database import get_guild_settings

class NoPermVCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def onMemberUpdate(self, member)
        for voicechannel in member.guild.voice_channels:
            for user in voicechannel.VoiceChannel.members:
                if user == member:
                    permissions = VoiceChannel.permissions_for(member)
        for permission in permissions:
            if permission != Permissions.speak:


