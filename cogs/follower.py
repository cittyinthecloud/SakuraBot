import concurrent.futures
from typing import Optional

import aiohttp
from discord import Guild, Role
from discord import utils
from discord.ext import commands
from twitch import TwitchClient

from SECRET import twitch_client_id
from models import UserData
from utils.database import get_guild_settings
from requests.exceptions import HTTPError

client: TwitchClient = TwitchClient(client_id=twitch_client_id)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
streamerids = {}


def is_following(streamer: str, memberid: str):
    if streamer not in streamerids:
        ret = client.users.translate_usernames_to_ids([streamer])
        if len(ret) == 0:
            return False
        else:
            streamerids[streamer] = ret[0]["id"]
    try:
        return client.users.check_follows_channel(memberid, streamerids[streamer])
    except HTTPError:
        return False



class TwitchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def guild_check(self, guild: Guild):
        settings = await get_guild_settings(guild)
        if settings.sync_twitch_followers:
            streamername: str = settings.twitch_account_name
            followerrole: Optional[Role] = utils.get(guild.roles, name=settings.follower_role_name)
            if followerrole is None:
                return

            for member in guild.members:
                # The following would work if discord allowed bots to check linked accounts.
                #
                # profile = await member.profile()
                # for acc in profile.connected_accounts:
                #     if acc["type"] == "twitch":
                #         following = await self.bot.loop.run_in_executor(executor, is_following, streamername, acc["id"])
                #
                #         if following and followerrole not in member.roles:
                #                 #             await member.add_roles(followerrole)
                #                 #         elif not following and followerrole in member.roles:
                #                 #             await member.remove_roles(followerrole)
                query = UserData.filter(user_id=str(member.id))

                if await query.count() < 1:
                    continue
                else:

                    following = await self.bot.loop.run_in_executor(
                        executor, is_following, streamername, (await query.first()).twitch_account_id
                    )

                    if following and followerrole not in member.roles:
                        await member.add_roles(followerrole)
                    elif not following and followerrole in member.roles:
                        await member.remove_roles(followerrole)

    @commands.command()
    async def followerrefresh(self, ctx: commands.Context):
        if ctx.guild is None:
            return await ctx.send("This command must be done in a guild")

        await self.guild_check(ctx.guild)

        await ctx.send("Guild follower updated")

    @commands.command()
    async def mytwitchis(self, ctx: commands.Context, username: str):
        ret = await self.bot.loop.run_in_executor(executor, client.users.translate_usernames_to_ids, [username])
        if len(ret) < 1:
            return await ctx.send(f"Could not find twitch user with name {username}")
        userdata: UserData = (
            await UserData.get_or_create(defaults={"twitch_account_id": ret[0]["id"]}, user_id=ctx.author.id)
        )[0]
        userdata.twitch_account_id = ret[0]["id"]
        await userdata.save()
        return await ctx.send(f"Your twitch account has been set to {username}")


def setup(bot):
    bot.add_cog(TwitchCog(bot))

