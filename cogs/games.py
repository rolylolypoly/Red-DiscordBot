import discord
import json
from discord.ext import commands
from .utils.dataIO import dataIO

def GameRanks:
    """Allows users to recieve select roles on command."""

    def __init__(self, bot):
        self.bot = bot;
        try:
            self.games = dataIO.load_json('data/ranks/ranks.json')
        except FileNotFoundError:
            self.games = {}

    def write_json(self):
        dataIO.save_json('data/ranks/ranks.json', self.ranks);

    async def gamedebug(self, ctx):
        server = ctx.message.server
        self.bot.say(ctx.message.author)
        for _,key in vars(server).iteritems():
            self.bot.say(key)

    @commands.command()
    async def game(self, ctx, role : discord.Role):
        """Allows a user to add themselves to a rank."""
        server = ctx.message.server
        if not server.id in self.games or not role.name in self.games[server.id]:
            self.bot.say('The requested role is not available as a game')
        else:
            self.bot.say('todo')

    @Commands.command()
    @checks.mod_or_permissions(manage_server=True)
    async def addgame(self, ctx, role : discord.Role):
        """Administration of joinable ranks."""
        server = ctx.message.server
        if not server.id in self.games:
            self.games[server.id] = []
        self.games[server.id].append(role.name)
        self.write_json()



def setup(bot):
    bot.add_cog(GameRanks(bot))
