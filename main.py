from discord.ext import commands
from discord.ext.commands import Bot
import sys
import traceback
import logging
from SECRET import bot_token
from tortoise import Tortoise

init_extensions = ["cogs.basic"]

logging.basicConfig(level=logging.INFO)

bot: Bot

async def asyncinit():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules=dict(models=["models"])
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    bot = commands.Bot(command_prefix=commands.when_mentioned_or("&"))
    bot.loop.run_until_complete(asyncinit())
    for ext in init_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {ext}", file=sys.stderr)
            traceback.print_exc()

    