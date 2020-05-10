import os

import aiohttp
import discord
from discord.ext import commands

from utils import default


class osu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        
    @commands.command()
    async def osu(self, ctx, player_id):
        """ Sends osu stats of username. """
        osu_api_key = self.config.osukey
        async with aiohttp.ClientSession() as session:
            async with session.get("https://osu.ppy.sh/api/get_user", params={"k": osu_api_key, "u": player_id}) as resp:
                resp.raise_for_status()
                payload = await resp.json()
        if len(payload) == 0:
            await ctx.send(f'cyka blyat! couldn\'t find any user matching this name / ID.')
        else:
            user = payload[0]

            USERNAME = user["username"]
            USERID = user["user_id"]
            JOINDATE = user["join_date"]
            PLAYCOUNT = user["playcount"]
            PPRAW = user["pp_raw"]
            PPRANK = user["pp_rank"]
            COUNTRYRANK = user["pp_country_rank"]
            LEVEL = user["level"]
            COUNTRY = user["country"]

            country = COUNTRY.lower()
            a0 = float(LEVEL)
            a1 = int(a0)
            b0 = float(PLAYCOUNT)
            b1 = int(b0)
            c0 = float(PPRAW)
            c1 = int(c0)

            userinfo=f"""Joined {JOINDATE}
Level: `{a1}`
Ranked games count: `{b1}`
Country: :flag_{country}:"""
            
            ranking=f"""Total performance points : `{c1}`
Global ranking: `#{PPRANK}`
Country ranking: `#{COUNTRYRANK}`"""
            
            e = discord.Embed(title = f'{USERNAME}', description=f'ID: {USERID}', url = f'https://osu.ppy.sh/users/{USERID}', color = 0xFF69B4)
            e.set_author(name="osu! profile info", icon_url='https://up.ppy.sh/files/osu-36.png')
            e.add_field(name='User info', value=userinfo)
            e.add_field(name='Ranking', value=ranking)
            e.set_thumbnail(url=f'https://a.ppy.sh/{USERID}')
            await ctx.send(embed = e)


def setup(bot):
    bot.add_cog(osu(bot))