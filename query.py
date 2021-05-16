from sql import SqlModule
import os


class QueryModule(SqlModule):
    def connect_sql(self):
        super().connect_sql()
        self.query_filepath = './query'

    async def send_query(self, cmd, args=None, multi=False):
        if args is None:
            args = []
        path = os.path.join(self.query_filepath, cmd + '.sql')
        if not os.path.isfile(path):
            print('Query not found')
            return None
        else:
            with open(path, 'r') as f:
                try:
                    query = f.read().strip().format(*args)
                except IndexError:
                    print('args invalid')
                    return None
            return await self.send_sqlquery(query, multi)

    def format_table(self, table):
        output = '\n--------------------\n'
        for row in table:
            for word in row:
                output += word + '  '
            output += '\n'
        output += '--------------------'
        return output

