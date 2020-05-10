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

            if "Unauthorized" in str(err) and len(ctx.message.clean_content):
                return await ctx.send(
                    f"the error was over 2000 characters, or the error leaked a token.\n"
                    f"error will not be displayed."
                )

            await print(f"cyka blyat! there was an error.\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send(f"cyka blyat! you're being ratelimited due to your command usage at a time, please finish the previous one.")

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"cyka blyat! this command is on cooldown. try again in {err.retry_after:.2f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} | {ctx.author} | {ctx.message.clean_content}")
        except AttributeError:
            print(f"DM | {ctx.author} | {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_ready(self):
        """ The function that actiavtes when boot was completed """
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        # Indicate that the bot has successfully booted up
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}')

        await self.bot.change_presence(activity=discord.Activity(type=3, name=f"{len(self.bot.guilds)} servers | cyka blyat!"), status=discord.Status.online)

    @commands.Cog.listener()	
    async def on_guild_join(self, guild):
        print(f'I have joined a guild. | Guilds: {len(self.bot.guilds)}')
        if not self.config.join_message:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config.join_message)
        await self.bot.change_presence(activity=discord.Activity(type=3, name=f"{len(self.bot.guilds)} servers | cyka blyat!"), status=discord.Status.online)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f'I have been removed from a guild. | Guilds: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Activity(type=3, name=f"{len(self.bot.guilds)} servers | cyka blyat!"), status=discord.Status.online)


def setup(bot):
    bot.add_cog(Events(bot))
