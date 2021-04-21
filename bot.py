import json
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound


class DiscordBot:
    def __init__(self):
        self.token = ''
        self.bot = commands.Bot(command_prefix='>')

    def __read_data(self):
        if os.path.isfile('token.json'):
            with open('token.json', 'r') as f:
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

    # React function

    def thumbs_up(self, ctx):
        pass

    def thumbs_down(self, ctx):
        pass

    async def send_back(self, ctx, msg):
        await ctx.send(f'>>> {msg}')

    # Callable function

    def start_bot(self):
        self.__read_data()
        self.__set_command()
        print('Staring bot ...')
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
