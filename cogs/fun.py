import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re

from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default, argparser


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command(aliases=['eightball', '8ball'])
    async def slavball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"**Question:** {question}\n**Answer:** {answer}")

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: str):
        """ Find the 'best' definition to your words """
        async with ctx.channel.typing():
            url = await http.get(f'https://api.urbandictionary.com/v0/define?term={search}', res_method="json")

            if url is None:
                return await ctx.send("cyka blyat! API broke.")

            if not len(url['list']):
                return await ctx.send("cyka blyat! couldn't find your search in the dictionary...")

            result = sorted(url['list'], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result['definition']
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

            await ctx.send(f"Definitions for **{result['word']}**```fix\n{definition}```")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ .txet esreveR
        Everything you type after reverse will be reversed.
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"{t_rev}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"i rate {thing} a **{num}.{deci} / 100**")


def setup(bot):
    bot.add_cog(Fun(bot))
