import discord
from models import GuildSettings

default_guild_settings = {"sync_twitch_followers": False, "twitch_account_name": "", "follower_role_name": "", "kick_on_losing_connect_perms": True}


async def get_guild_settings(guild: discord.Guild):
    return (await GuildSettings.get_or_create(defaults=default_guild_settings, guild_id=str(guild.id)))[0]
