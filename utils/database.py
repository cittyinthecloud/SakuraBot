from discord import Guild
from models import GuildSettings


async def get_guild_settings(guild: Guild):
    "Gets the settings for a guild"
    return await GuildSettings.get_or_create(
        defaults=dict(synctwitchfollowers=False, twitchaccountname=""), guildid=guild.id
    )
    