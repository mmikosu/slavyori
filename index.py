import os
import discord

from discord.ext.commands import DefaultHelpCommand
from data import Bot
from utils import permissions, default

config = default.get("config.json")


class HelpFormat(DefaultHelpCommand):
    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author


print("Logging in...")
bot = Bot(command_prefix=config.prefix, prefix=config.prefix, command_attrs=dict(hidden=True), help_command=HelpFormat())

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(config.token)
