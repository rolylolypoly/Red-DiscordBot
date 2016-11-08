import os
import discord
import time
import uuid
from cogs.utils.dataIO import dataIO
from discord.ext import commands

class DB:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dbfiletest(self):
        try:
            await self.bot.say(dataIO.load_json("data.txt"))
        except FileExistsError or FileNotFoundError:
            await dataIO.save_json("data.txt")
            await self.bot.say("Check the fucking file")

def setup(bot):
    bot.add_cog(DB(bot))
