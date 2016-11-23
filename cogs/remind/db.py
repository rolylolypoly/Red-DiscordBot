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
table = 'table'  # name of the table to be created
field = 'test'  # name of the column
field_type = 'INTEGER'  # column data type


class DB:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dbfiletest(self):
        try:
            c.execute(
                'SELECT * FROM {tn}'
            )
            results = c.fetchall()
            await self.bot.say(results)

        except FileExistsError or FileNotFoundError:
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
    bot.add_cog(DB(bot))
