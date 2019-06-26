import subprocess

import discord
from discord import utils
from discord.ext import commands

from models import GuildSettings
from utils.database import get_guild_settings


class BasicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def version(self, ctx: commands.Context):
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
    async def settings(self, ctx: commands.Context):
        if ctx.guild is None:
            return await ctx.send("This command must be run in a guild")
        embed: discord.Embed = discord.Embed(name="Current settings for guild")

        settings: GuildSettings = await get_guild_settings(ctx.guild)

        embed.add_field(name="Sync Twitch Followers", value=str(settings.sync_twitch_followers))
        embed.add_field(name="Twitch Account Username", value=repr(settings.twitch_account_name))
        embed.add_field(name="Follower Role Name", value=repr(settings.follower_role_name))
        embed.add_field(
            name="Kick Users from VC when they lose connect perms", value=str(settings.kick_on_losing_connect_perms)
        )
        return await ctx.send(embed=embed)

    @settings.command()
    async def twitch(self, ctx: commands.Context, username: str):
        if ctx.guild is None:
            return await ctx.send("This command must be run in a guild")

        settings: GuildSettings = await get_guild_settings(ctx.guild)
        settings.twitch_account_name = username
        await settings.save()

        return await ctx.send(f"Twitch username changed to: {settings.twitch_account_name}")

    @settings.command()
    async def followerrole(self, ctx: commands.Context, role_name: str):
        if ctx.guild is None:
            return await ctx.send("This command must be run in a guild")

        if utils.get(ctx.guild.roles, name=role_name) is None:
            return await ctx.send(f"The role {role_name} doesn't exist")

        settings: GuildSettings = await get_guild_settings(ctx.guild)
        settings.follower_role_name = role_name
        await settings.save()

        return await ctx.send(f"Twitch Follower Role changed to: {settings.follower_role_name}")

    @settings.command()
    async def followersync(self, ctx: commands.Context):
        if ctx.guild is None:
            return await ctx.send("This command must be run in a guild")

        settings: GuildSettings = await get_guild_settings(ctx.guild)
        settings.sync_twitch_followers = not settings.sync_twitch_followers
        await settings.save()

        return await ctx.send(
            f"Twitch Follower Role Sync has been {'enabled' if settings.sync_twitch_followers else 'disabled'}."
        )

    @settings.command()
    async def voicekick(self, ctx: commands.Context):
        if ctx.guild is None:
            return await ctx.send("This command must be run in a guild")

        settings: GuildSettings = await get_guild_settings(ctx.guild)
        settings.kick_on_losing_connect_perms = not settings.kick_on_losing_connect_perms
        await settings.save()

        return await ctx.send(
            f"Kicking members from voice channels on lost connect permissions has been "
            f"{'enabled' if settings.kick_on_losing_connect_perms else 'disabled'}."
        )


def setup(bot):
    bot.add_cog(BasicCog(bot))
