import logging
import sys
import traceback

from discord.ext import commands
from discord.ext.commands import Bot
from tortoise import Tortoise

from SECRET import bot_token

init_extensions = ["cogs.basic", "cogs.nopermvc", "cogs.follower", "cogs.privatechan"]

logging.basicConfig(level=logging.INFO)

bot: Bot = commands.Bot(command_prefix=commands.when_mentioned_or("&"))


async def asyncinit():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules=dict(models=["models"]))
    await Tortoise.generate_schemas()


if __name__ == "__main__":

    bot.loop.run_until_complete(asyncinit())
    for ext in init_extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(f"Failed to load extension {ext}", file=sys.stderr)
            traceback.print_exc()
    bot.run(bot_token)
