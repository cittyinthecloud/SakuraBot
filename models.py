from tortoise.models import Model
from tortoise import fields
import discord
class GuildSettings(Model):
    guildid = fields.CharField(18, pk=True)
    synctwitchfollowers = fields.BooleanField()
    twitchaccountname = fields.TextField()