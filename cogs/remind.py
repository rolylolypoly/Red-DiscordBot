import os
import json
import discord
from discord.ext import commands


class Remind:
    def __init__(self, bot):
        self.bot = bot

    async def jsonwrite(self, data):
        await self.bot.say(os.getcwd())
        await self.bot.say(data)
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

    async def parse1(self, potato):
        await self.bot.say(potato)
        await self.bot.say(potato[0])
        await self.bot.say(potato[1])
        await self.bot.say(potato.index("at", 2, potato.__len__()) + 1)
        await self.bot.say(potato[(potato.index("at", 2, potato.__len__()) + 1):])
        await self.bot.say(''.join(str(e) + " " for e in potato[2, potato.__len__()]))

    async def parse2(self, recipient, message, time, meta):
        data = {"recipient": recipient, "message": message, "time": time, "meta": meta}
        self.jsonwrite(data)

    @commands.command()
    async def jsonread(self):
        await self.bot.say(os.getcwd())
        with open('data.txt') as infile:
            data = (json.load(infile))
        await self.bot.say(data)

    @commands.command(pass_context=True)
    async def remind(self, ctx, *poop):
        """This is supposed to do stuff."""
        author = ctx.message.author
        await self.bot.say("I will remind " + author.mention)
        await self.parse1(poop)

    @commands.command()
    async def pwd(self):
        await self.bot.say(os.getcwd())

    @commands.command()
    async def datatest(self):
        data = [1, 2, 3, 4, 5]
        await self.jsonwrite(data)


def setup(bot):
    bot.add_cog(Remind(bot))
