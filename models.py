from tortoise.models import Model
from tortoise import fields


class GuildSettings(Model):
    guild_id = fields.CharField(18, pk=True)
    sync_twitch_followers = fields.BooleanField()
    twitch_account_name = fields.TextField()
    follower_role_name = fields.CharField(255)
    kick_on_losing_connect_perms = fields.BooleanField()


class UserData(Model):
    user_id = fields.CharField(18, pk=True)
    twitch_account_id = fields.TextField()
