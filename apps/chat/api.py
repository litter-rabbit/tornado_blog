from ..baseHandler import BaseHandler
import tornado.websocket
import datetime
import json
import time
class IndexHandle(BaseHandler):

    def get(self):
        chat_num = self.application.redis.get('chat:num')
        messages = self.application.redis.zrange('message',0,-1)
        messages = map(lambda k:json.loads(k),messages)


        self.render('chat/index.html',chat_num=chat_num,messages=messages)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        ChatSocketHandler.waiters.add(self)
        self.application.redis.incr('chat:num')

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)
        self.application.redis.decr('chat:num')

    def on_message(self, message):

        message_dict = {'text':message, 'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.application.redis.zadd('message',int(time.time()),json.dumps(message_dict))


        ChatSocketHandler.send_updates(message_dict)

    @classmethod
    def send_updates(cls, message_dict):
        print("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(message_dict)
            except:
                print('推送更新失败')




