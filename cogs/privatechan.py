import time
from dataclasses import dataclass
from typing import Optional, Dict

import discord
from discord import utils
from discord.ext import commands
from discord.ext.commands import Greedy


@dataclass()
class PrivateChanInvite:
    uses: int
    channel: discord.TextChannel
    max_uses: int


pc_invites: Dict[str, PrivateChanInvite] = {}


class SocialCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        elif utils.get(ctx.guild.roles, name="PrivateChan") in ctx.author.roles:
            return True
        elif ctx.author.guild_permissions.manage_channels:
            return True
        else:
            return False

    @commands.group(invoke_without_command=True, name="privatechan")
    async def private_chan(self, ctx: commands.Context):
        await ctx.send(
            "```"
            "privatechan create [user] ([user] ...)\n"
            "privatechan add [user] (in a private channel)\n"
            "privatechan close\n"
            "privatechan kick [user]\n"
            "privatechan invitelink (max_uses) default maxuses is 1```"
        )

    @commands.guild_only()
    @private_chan.command()
    async def create(self, ctx: commands.Context, members: Greedy[discord.Member]):
        private_cat: Optional[discord.CategoryChannel] = utils.get(ctx.guild.categories, name="PrivateChan")
        if private_cat is None:
            private_cat = await ctx.guild.create_category(name="PrivateChan")

        members.append(ctx.author)
        members.append(ctx.me)
        overwrites = {member: discord.PermissionOverwrite(read_messages=True) for member in members}
        overwrites[ctx.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
        private_channel: discord.TextChannel = await private_cat.create_text_channel(
            name=f"private-chan-{str(time.clock())}", overwrites=overwrites
        )
        members.remove(ctx.author)
        members.remove(ctx.me)
        await private_channel.send(
            f"{ctx.author.mention} created this private channel with {', '.join(map(str,members))}"
        )

    @commands.guild_only()
    @private_chan.command()
    async def kick(self, ctx: commands.Context, member: discord.Member):
        if ctx.channel.category is not None and ctx.channel.category.name == "PrivateChan":
            await ctx.channel.set_permissions(member, read_messages=False)
            await ctx.channel.send(f"Kicked {member.mention} from the channel")

    @commands.guild_only()
    @private_chan.command(aliases=["invite"])
    async def add(self, ctx: commands.Context, member: discord.Member):
        if ctx.channel.category is not None and ctx.channel.category.name == "PrivateChan":
            await ctx.channel.set_permissions(member, read_messages=True)
            await ctx.channel.send(f"Added {member.mention} to the channel")

    @commands.guild_only()
    @private_chan.command(aliases=["delete"])
    async def close(self, ctx: commands.Context):
        if ctx.channel.category is not None and ctx.channel.category.name == "PrivateChan":
            await ctx.channel.delete()

    @commands.guild_only()
    @private_chan.command()
    async def name(self, ctx: commands.Context, name):
        if ctx.channel.category is not None and ctx.channel.category.name == "PrivateChan":
            await ctx.channel.edit(name=name)

    @commands.guild_only()
    @private_chan.command(aliases=["topic"])
    async def desc(self, ctx: commands.Context, *, topic):
        if ctx.channel.category is not None and ctx.channel.category.name == "PrivateChan":
            await ctx.channel.edit(topic=topic)

    @commands.guild_only()
    @private_chan.command(name="invitelink")
    async def invite_link(self, ctx: commands.Context, max_uses: Optional[int] = 1):
        if ctx.channel.category is not None and ctx.channel.category.name == "PrivateChan":
            invite = await ctx.channel.create_invite(reason="PrivateChan invite", max_uses=max_uses + 1)
            pc_invites[invite.code] = PrivateChanInvite(max_uses=max_uses, uses=invite.uses, channel=ctx.channel)
            await ctx.send(f"Channel invite created: {invite.url}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        for d_invite in await member.guild.invites():
            if d_invite.code in pc_invites:
                pc_invite = pc_invites[d_invite.code]
                if d_invite.uses != pc_invite.uses:
                    pc_invite.uses = d_invite.uses
                    await pc_invite.channel.set_permissions(member, read_messages=True)
                    await pc_invite.channel.send(f"{member.mention} joined the channel via invite {d_invite.code}")
                    if pc_invite.uses >= pc_invite.max_uses:
                        await pc_invite.channel.send(f"Channel invite {d_invite.code} has been used up.")
                        del pc_invites[d_invite.code]
                        await d_invite.delete()


def setup(bot: commands.Bot):
    bot.add_cog(SocialCog(bot))
