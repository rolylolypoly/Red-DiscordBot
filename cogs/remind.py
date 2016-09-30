import os
import discord
import time
from .utils.dataIO import dataIO
from discord.ext import commands


class Remind:
    Tick = False

    def __init__(self, bot):
        self.bot = bot

    async def hello(self, string: str):
        await self.bot.say('hello {} ({:.4f})'.format(string, time.time()))
        time.sleep(.3)

    async def do_every(self, period, function, *args):
        def g_tick():
            t = time.time()
            count = 0
            while self.Tick:
                count += 1
                yield max(t + count * period - time.time(), 0)

        g = g_tick()
        while self.Tick:
            time.sleep(next(g))
            await function(*args)

    async def parse1(self, string, author):

        await self.parse2(string[0],
                          string[2],
                          string[string.index('at')],
                          author)

    async def parse2(self, recipient, message, when, author):
        data = {"recipient": recipient,
                "message": message,
                "when": when,
                "meta":
                    {"timestamp": time.time(),
                     "author": author
                     }
                }
        await dataIO.save_json('data.txt', data)

    @commands.command()
    async def ticktest(self, state: str):
        if state.lower() == "on":
            self.Tick = True
            await self.bot.say("On.")
        elif state.lower() == "off":
            self.Tick = False
            await self.bot.say("Off.")
        else:
            await self.bot.say(self.Tick)
            await self.do_every(1, self.hello, 'bweep')

    @commands.command(pass_context=True)
    async def remind(self, ctx, *poop):
        """This is supposed to do stuff."""
        author = ctx.message.author
        if poop == 'list':
            await self.bot.say(dataIO.load_json('data.txt'))
        else:
            await self.parse1(poop, author)

    @commands.command()
    async def pwd(self):
        await self.bot.say(os.getcwd())

    @commands.command()
    async def datatest(self):
        data = [1, 2, 3, 4, 5]
        await dataIO.save_json('data.txt', data)


def setup(bot):
    bot.add_cog(Remind(bot))
