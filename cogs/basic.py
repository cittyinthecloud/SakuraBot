import subprocess

import discord
from discord.ext import commands
from utils.database import get_guild_settings

class BasicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def version(ctx: commands.Context):
        commithash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        embed = discord.Embed(
            title="Bot Version",
            color=discord.Color(0x8E8252),
            description=f"We are running SakuraBot commit `{commithash.decode('ascii').strip()}`",
        )
        embed.add_field("Authors", "famous1622 and SnowyTSW")
        embed.set_footer(text="famousBots discord: https://discord.gg/PPSra9d")
        return await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def settings(ctx:commands.context):
        if ctx.guild is None:
            return await ctx.send("This command must be run in a guild")
        embed: discord.Embed = discord.Embed(name="Current settings for guild")
        
        settings: GuildSettings = await get_guild_settings(ctx.guild)

        discord.Embed.add_field()
        embed.add_field("Sync Twitch Followers", settings.synctwitchfollowers)
        embed.add_field("Twitch Account Username", settings.twitchaccountusername)        