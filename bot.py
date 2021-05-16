import json
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord import Embed


class BotModule:
    def __init__(self):
        self.token = ''
        self.bot = commands.Bot(command_prefix='>')
        self.prefix = '>'

    def __read_data(self):
        if os.path.isfile('config/token.json'):
            with open('config/token.json', 'r') as f:
                data = json.load(f)
            self.token = data['TOKEN']
            if self.token == "":
                print('Token invalid')
        else:
            print('Token file not found')

    def __set_command(self):
        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} has connected to Discord')

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, CommandNotFound):
                await self.send_back(ctx, f'Command not found. Use `{self.bot.command_prefix}help` to see the command list.')
                return
            raise error

    # Reply function

    async def react_yes(self, ctx):
        await ctx.message.add_reaction("✅")

    async def react_no(self, ctx):
        await ctx.message.add_reaction("🚫")

    async def send_back(self, ctx, msg, embed=False):
        if embed:
            e = Embed()
            e.title = 'Thank you!'
            e.description = msg
            return await ctx.send(embed=e)
        else:
            return await ctx.send(f'>>> {msg}')

    async def send_embed(self, ctx, embed):
        return await ctx.send(embed=embed)

    # Callable function

    def start_bot(self):
        self.__read_data()
        self.__set_command()
        print('Starting bot ...')
        self.bot.run(self.token)

    def add_func(self, cmd, func, arg_parse=True):
        setattr(self, cmd, func)
        if arg_parse:
            @self.bot.command(name=cmd)
            async def f(ctx, *args):
                await getattr(self, cmd)(ctx, args)
        else:
            @self.bot.command(name=cmd)
            async def f(ctx, *, args):
                await getattr(self, cmd)(ctx, args)
