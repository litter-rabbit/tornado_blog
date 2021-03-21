import redis

#redis = redis.StrictRedis(host='127.0.0.1',db=1,decode_responses=True)
redis = redis.StrictRedis(host='121.199.4.165',db=1,decode_responses=True)

def show_message():

    messages = redis.zrange('message',0,-1,desc=True)

    for m in messages:
        print(m)

def delete_message_by_value(text,all=False):
    if not all:
        if redis.zrem('message',text):
            print('删除成功',text)
    else:
        c = input('你确认删除所有的消息吗yes/no')
        if c=='yes':
            messages = redis.zrange('message',0,-1)
            for m in messages:
                if redis.zrem('message',m):
                    print('删除成功',m)
        else:
            print('删除取消')



if __name__ == '__main__':
    show_message()
    #delete_message_by_value('{"text": "213", "time": "2021-02-05 01:30:18"}')

