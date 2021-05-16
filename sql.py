import mysql.connector
import json
from mysql.connector.errors import DatabaseError, ProgrammingError


class SqlModule:
    def __del__(self):
        if self.mydb:
            self.mydb.close()

    def __read_config(self):
        with open('config/config.json', 'r') as f:
            data = json.load(f)
            self.HOST = data['HOST']
            self.PORT = data['PORT']
            self.USER = data['USER']
            self.PASS = data['PASS']
            self.DB = data['DB']

    def connect_sql(self):
        try:
            self.__read_config()
            self.mydb = mysql.connector.connect(
                host=self.HOST,
                port=self.PORT,
                user=self.USER,
                password=self.PASS,
                database=self.DB
            )
        except DatabaseError:
            print('Cannot connect to the server')
            return False
        self.mycursor = self.mydb.cursor()
        return True

    def update_db(self):
        self.mydb.commit()

    async def send_sqlquery(self, query, multi):
        try:
            if multi:
                for result in self.mycursor.execute(query, multi=multi):
                    pass
            else:
                self.mycursor.execute(query)
            result = [row for row in self.mycursor]
            return result
        except ProgrammingError:
            print('The SQL syntax is invalid')
            return None
