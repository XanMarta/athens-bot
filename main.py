from bot import BotModule
from query import QueryModule
from discord import Embed
from discord.errors import NotFound
import os, json


class MainProgram(BotModule, QueryModule):
    def __init__(self):
        super().__init__()
        if os.path.isfile('./config/server.json'):
            with open('./config/server.json', 'r') as f:
                data = json.load(f)
            self.tracker_channel = data["tracker_channel"]
        else:
            print('Server config file not found')

    def start(self):
        self.connect_sql()
        self.set_method()
        self.start_bot()

    def set_method(self):
        async def request(ctx, args):
            await self.__check_user(ctx.message.author)
            requestLink = ctx.message.jump_url
            content = args
            requesterID = ctx.message.author.id
            result = await self.send_query('request', [requestLink, content, requesterID])
            if result is not None:
                self.update_db()
                check_id = await self.send_query('checkautoid')
                taskID = check_id[0][0] - 1
                link = await self.__update_tracker(taskID)
                await self.react_yes(ctx)
                await self.send_back(ctx, f'Your request has been recorded. '
                                          f'You can check your request [here]({link})', embed=True)
            else:
                await self.react_no(ctx)
        self.add_func('request', request, arg_parse=False)

        async def complete(ctx, args):
            await self.__check_user(ctx.message.author)
            if len(args) != 2:
                await self.react_no(ctx)
                await self.send_back(ctx, 'Command needs 2 arguments: taskID and messageLink')
            else:
                taskID = args[0]
                completeLink = args[1]
                completerID = ctx.message.author.id
                result = await self.send_query('searchpost', [taskID])
                if result is not None:
                    if len(result) > 0:
                        await self.react_no(ctx)
                        await self.send_back(ctx, 'Sorry. The request was completed before.')
                    else:
                        result = await self.send_query('complete', [taskID, completeLink, completerID])
                        if result is None:
                            await self.react_no(ctx)
                            await self.send_back(ctx, 'taskID invalid')
                        else:
                            await self.send_query('setstatus', ['completed', taskID])
                            link = await self.__update_tracker(taskID)
                            await self.react_yes(ctx)
                            await self.send_back(ctx, f'Thank for completing request! '
                                                      f'You can check your completed post [here]({link})', embed=True)
                self.update_db()
        self.add_func('complete', complete)

        async def _delete(ctx, args):
            await self.__check_user(ctx.message.author)
            if len(args) != 1:
                await self.react_no(ctx)
                await self.send_back(ctx, 'Command needs 1 argument: taskID')
            else:
                taskID = args[0]
                info = await self.send_query('info', [taskID])
                if info is not None:
                    link, requesterID, content, status, requestLink, completerID, completeLink = info[0]
                    if status == "completed" or int(requesterID) != ctx.message.author.id:
                        await self.react_no(ctx)
                        await self.send_back(ctx, 'You have no right to delete the request.')
                    else:
                        result = await self.send_query('deletetask', [taskID, taskID, taskID], multi=True)
                        if result is not None:
                            self.update_db()
                            message = await self.get_message(link)
                            if message is not None:
                                await message.delete()
                            await self.react_yes(ctx)
                            await self.send_back(ctx, f'Task {taskID} is completely deleted.')
        self.add_func('delete', _delete)

        async def _list(ctx, args):
            await self.__check_user(ctx.message.author)
            if not len(args) in [1, 2, 3]:
                await self.react_no(ctx)
                await self.send_back(ctx, 'Wrong argument. Command: list <[status] [user]> [start_record]')
            else:
                status = userID = ''
                start = 1
                for arg in args:
                    if arg in ['requesting', 'holding', 'completed', 'reported']:
                        status = arg
                    elif arg.startswith('<@!'):
                        userID = arg.lstrip('<@!').rstrip('>')
                    else:
                        try:
                            start = int(arg)
                            if start < 1:
                                start = 1
                        except ValueError:
                            pass
                if status != '' or userID != '':
                    if userID == '':
                        result = await self.send_query('lists', [status])
                    elif status == '':
                        result = await self.send_query('listu', [userID])
                    else:
                        result = await self.send_query('listsu', [userID, status])
                    if result is not None:
                        s_taskID = s_requesterID = s_link = ''
                        end = 0
                        for row in result:
                            end += 1
                            if end >= start:
                                if row[2] is not None:
                                    link = f'[LINK]({row[2]})'
                                else:
                                    link = '*not found*'
                                if len(s_link) + len(link) > 1000:
                                    break
                                s_taskID += str(row[0]) + '\n'
                                s_requesterID += f'<@{row[1]}>' + '\n'
                                s_link += link + '\n'
                        s_taskID += '----------'
                        s_requesterID += '----------'
                        s_link += '----------'
                        embed = Embed()
                        embed.title = f'{len(result)} {status} tasks found. Show [{start if end != 0 else 0} - {end}]'
                        embed.add_field(name='taskID', value=s_taskID)
                        embed.add_field(name='requester', value=s_requesterID)
                        embed.add_field(name='link', value=s_link)
                        await self.react_yes(ctx)
                        await self.send_embed(ctx, embed=embed)
                else:
                    await self.react_no(ctx)
                    await self.send_back(ctx, 'Wrong argument. Command: list <[status] [user]> [start_record]')
        self.add_func('list', _list)

        async def rank(ctx, args):
            await self.__check_user(ctx.message.author)
            number = 10
            if len(args) == 1:
                try:
                    number = int(args[0])
                    if not number in range(1, 31):
                        await self.send_back(ctx, 'Wrong range. Valid range is [1, 30]. Use 10 instead')
                        number = 10
                except ValueError:
                    pass
            result = await self.send_query('rank', [number])
            if result is not None:
                s_rank = s_userID = s_total = ''
                count = 0
                for row in result:
                    count += 1
                    s_rank += str(count) + '\n'
                    s_userID += f'<@{row[0]}>' + '\n'
                    s_total += str(row[1]) + '\n'
                s_rank += '----------'
                s_userID += '----------'
                s_total += '----------'
                embed = Embed()
                embed.title = f'Rank of {len(result)} best completers'
                embed.add_field(name='Rank', value=s_rank)
                embed.add_field(name='User', value=s_userID)
                embed.add_field(name='Point', value=s_total)
                await self.react_yes(ctx)
                await self.send_embed(ctx, embed)
        self.add_func('rank', rank)

        async def hello(ctx, args):
            await self.send_back(ctx, 'Hi there!')
        self.add_func('hello', hello)

        async def show(ctx, args):
            await self.__check_user(ctx.message.author)
            embed = Embed()
            embed.title = 'List of commands'
            cmd = f'**{self.prefix}request** <content>\n' \
                  f'**{self.prefix}complete** <ID> <completeLink>\n' \
                  f'**{self.prefix}delete** <ID>\n' \
                  f'**{self.prefix}list** <[User] [status]> [start_record]\n' \
                  f'**{self.prefix}rank** [range]\n' \
                  f'**{self.prefix}show**'
            usg = 'Request a task\n' \
                  'Complete a task\n' \
                  'Delete a your own uncompleted task\n' \
                  'Get a list of tasks by user or status or both\n' \
                  'Get the rank of top completer\n' \
                  'Show available commands'
            embed.add_field(name='Command', value=cmd)
            embed.add_field(name='Usage', value=usg)
            await self.react_yes(ctx)
            await self.send_embed(ctx, embed)
        self.add_func('show', show)

        async def _exit(ctx, args):
            await self.send_back(ctx, 'Good bye')
            self.mycursor.close()
            self.mydb.close()
            self.mydb.disconnect()
            exit(0)
        self.add_func('exit', _exit)

    # Private method
    # ----------------

    async def __check_user(self, author):
        result = await self.send_query('checkuser', [author.id, str(author), author.name, 'member'])
        if result is not None:
            if len(result) == 0:
                await self.send_query('adduser', [author.id, str(author), author.name, 'member'])
                self.update_db()

    async def __update_tracker(self, taskID):
        info = await self.send_query('info', [taskID])
        if info is not None:
            link, requesterID, content, status, requestLink, completerID, completeLink = info[0]
            embed = Embed()
            embed.title = f'ID: {taskID}'
            embed.add_field(name='Requester', value=f'<@{requesterID}>', inline=True)
            embed.add_field(name='Status', value=status, inline=True)
            embed.add_field(name='Request Link', value=f'[LINK]({requestLink})', inline=True)
            if completerID is not None:
                embed.add_field(name='Completer', value=f'<@{completerID}>', inline=True)
                embed.add_field(name='Complete Link', value=f'[LINK]({completeLink})', inline=True)
            embed.add_field(name='Content', value=content, inline=False)
            if link is None:
                link = await self.send_embed(self.bot.get_channel(self.tracker_channel), embed)
                link = link.jump_url
                await self.send_query('addlink', [taskID, link])
                self.update_db()
            else:
                message = await self.get_message(link)
                if message is not None:
                    await message.edit(embed=embed)
                else:
                    print('Tracker not found')
            return link
        else:
            return ''

    async def get_message(self, link):
        if link is None:
            return link
        else:
            arg = link.split('/')
            try:
                message = await self.bot.get_guild(int(arg[4])) \
                    .get_channel(int(arg[5])) \
                    .fetch_message(int(arg[6]))
                return message
            except NotFound:
                return None


if __name__ == '__main__':
    program = MainProgram()
    program.start()
