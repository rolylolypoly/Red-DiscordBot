import os
import discord
import time
import uuid

import sqlite3

from cogs.utils.dataIO import dataIO
from discord.ext import commands

conn = sqlite3.connect("data.txt")
c = conn.cursor()

file = 'data.sqlite'  # name of the sqlite database file
table = 'test'  # name of the table to be created
field = 'column'  # name of the column
field_type = 'INTEGER'  # column data type


class DB:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dbfiletest(self):
        if not os.path.isfile('data.sqlite'):
            conn = sqlite3.connect('data.sqlite')
            c = conn.cursor()
            await self.bot.say('Creating new database...')
            c.execute('CREATE TABLE {tn} ({nf} {ft})'
                      .format(tn=table, nf=field, ft=field_type))
            await self.bot.say('SQL committing...')
            conn.commit()
            conn.close()
            await self.bot.say('Done')
        elif os.path.isfile('data.sqlite'):
            self.bot.say('Attempting SQLite')
            conn = sqlite3.connect('data.sqlite')
            c = conn.cursor()
            c.execute(
                'SELECT * FROM {tn}'.format(tn=table))
            self.bot.say('SQLite Connected')
            results = c.fetchall()
            conn.commit()
            conn.close()
            await self.bot.say(results)
        else:
            await self.bot.say('You dun goofed')

def setup(bot):
    bot.add_cog(DB(bot))
