from bot import DiscordBot


class MainProgram(DiscordBot):
    def start(self):
        self.set_method()
        self.start_bot()

    def set_method(self):
        async def request(ctx, args):
            await self.send_back(ctx, f'Hello there. Num of args: {len(args)}')
        self.add_func('hello', request)


if __name__ == '__main__':
    program = MainProgram()
    program.start()
