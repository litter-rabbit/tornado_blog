from ..baseHandler import BaseHandler
import markdown
import setting
import tornado.escape
from html import unescape
import aiomysql
import tornado.web
import bcrypt
import tornado.ioloop


class IndexHandler(BaseHandler):

    async def get(self):
        id = self.application.redis.rpop('list:task_ids')
        res = {
            'status': 0
        }
        if id:
            data={'id':id}
            res['status'] = 1
            res['data']=data
        self.write(res)


class SubmitTask(BaseHandler):

    async def get(self):
        id = self.get_argument('task_id')
        self.application.redis.lpush('list:task_ids', id)
        res={'status':1,
             'Msg':'success'}
        self.write(res)

