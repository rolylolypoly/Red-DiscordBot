import os
import discord
import time
import uuid

import sqlite3

from .utils.dataIO import dataIO
from discord.ext import commands



file = 'data.sqlite'  # name of the sqlite database file
table = 'table'  # name of the table to be created
field = 'test'  # name of the column
field_type = 'INTEGER'  # column data type


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
                          string[2:string.index('at')],
                          string[(string.index('at') + 1):string.__len__()],
                          author)

    async def parse2(self, recipient, message, when, author):
        data = {str(when):
                    {"recipient": recipient,
                     "message": message,
                     "meta":
                         {"timestamp": time.time(),
                          "author": author,
                          "uuid": str(uuid.uuid4())
                          }
                     }
                }
        data.update(dataIO.load_json("data.txt"))
        dataIO.save_json('data.txt', data)
        await self.bot.say("Data saved.")

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
        if poop == 'list':
            await self.bot.say(dataIO.load_json('data.txt'))
        else:
            await self.parse1(poop, str(ctx.message.author.id))

    @commands.command()
    async def pwd(self):
        await self.bot.say(os.getcwd())

    @commands.command()
    async def datatest(self):
        await self.bot.say(dataIO.load_json("data.txt"))

    @commands.command(pass_context=True)
    async def mentiontest(self, ctx):
        server = ctx.message.server
        for member in list(server.members):
            if int(member.id).__eq__(141678385024729088):
                await self.bot.say(member.mention)
                await self.bot.say(ctx.message.author.id)

    @commands.command()
    async def dbfiletest(self):
        try:
            conn = sqlite3.connect("data.txt")
            c = conn.cursor()
            c.execute(
                'SELECT * FROM {tn}'.format(tn=table))
            results = c.fetchall()
            conn.commit()
            conn.close()
            await self.bot.say(results)

        except FileExistsError or FileNotFoundError:
            conn = sqlite3.connect("data.txt")
            c = conn.cursor()
            await self.bot.say("Creating new database...")
            c.execute('CREATE TABLE {tn} ({nf} {ft})'
                      .format(tn=table, nf=field, ft=field_type))
            await self.bot.say("SQL committing...")
            conn.commit()
            conn.close()
            await self.bot.say("Done")
        except PermissionError:
            await self.bot.say("Check the fucking permissions")


def setup(bot):
    bot.add_cog(Remind(bot))
