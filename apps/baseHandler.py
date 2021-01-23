import tornado
from tornado.web import RequestHandler
import tornado.escape
import datetime
import json
import aiomysql

class BaseHandler(RequestHandler):


    def initialize(self):

        self.set_default_headers()

    async def prepare(self):

        user_id = self.get_secure_cookie('current_user')
        user_id = tornado.escape.to_unicode(user_id)
        sql = "select * from author where id='{}'".format(user_id)
        print(sql)
        author = await self.query_one(sql)
        if author:
            self.current_user = author


    def set_default_headers(self) -> None:
        pass




    def get_escape_argument(self, q):
        value = self.get_argument(q, None)
        return aiomysql.escape_string(value) if value else value
    def get_escape_string(self,q):

        return aiomysql.escape_string(q) if q else ""

    def get_format_time(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_json_body(self, q):
        return json.loads(q)

    async def query(self, sql):
        await self.application.db.ping()
        async with self.application.db.cursor() as cursor:
            await cursor.execute(sql)
            results = await cursor.fetchall()
            return results

    async def query_one(self,sql):

        await self.application.db.ping()
        async with self.application.db.cursor() as cursor:
            await cursor.execute(sql)
            result = await cursor.fetchall()
            if result:
                return result[0]
            else:
                return None

    async def execute(self, sql):
        await self.application.db.ping()
        async with self.application.db.cursor() as cursor:
            await cursor.execute(sql)
            await self.application.db.commit()
