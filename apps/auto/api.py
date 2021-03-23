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
        response = self.application.redis.brpop('list:response',timeout=30)
        res['data']=[{'response':response}]
        self.write(res)



class PushResponse(BaseHandler):

    async def post(self):
        print('接受到response')
        response = self.get_body_argument('data')
        print('rseponse',response)
        self.application.redis.lpush('list:response',response)




