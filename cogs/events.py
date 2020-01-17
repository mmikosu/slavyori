import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors
from utils import default


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            error = default.traceback_maker(err.original)
            await ctx.send(f"cyka blyat! there was an error processing the command.\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"cyka blyat! this command is on cooldown. try again in {err.retry_after:.2f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            print(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ready: {self.bot.user} | Guilds: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Game(name=f"sy.help | on {len(self.bot.guilds)} servers!"))

    @commands.Cog.listener()	
    async def on_guild_join(self, guild):
        print(f'I have joined a guild. | Guilds: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Game(name=f"sy.help | on {len(self.bot.guilds)} servers!"))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f'I have been removed from a guild. | Guilds: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Game(name=f"sy.help | on {len(self.bot.guilds)} servers!"))


def setup(bot):
    bot.add_cog(Events(bot))
