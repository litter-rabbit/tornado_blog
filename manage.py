import tornado.options
import aiomysql
import sys
from make_app import create_app
import bcrypt
import tornado.ioloop
import tornado.escape
import setting


async def create_admin():

    async def execute(sql):
        async with aiomysql.connect(
                host=setting.db_host,
                port=setting.db_port,
                user=setting.db_user,
                password=setting.db_password,
                db=setting.db_database,
                cursorclass=aiomysql.cursors.DictCursor
        ) as db:
            await db.ping()
            async  with db.cursor() as cursor:
                await cursor.execute(sql)
                await db.commit()

    username, password = ("", "")
    while True:
        username = input('请输入用户名').strip()
        if not username:
            print('输入的用户名长度为0,请重新输入', )
        else:
            break

    while True:
        password = input('请输入密码').strip()
        if not password:
            print("输入的密码为0,请重新输入")
        else:
            break
    hashed_password = bcrypt.hashpw(tornado.escape.utf8(password), bcrypt.gensalt())
    hashed_password  = tornado.escape.to_unicode(hashed_password)
    sql = "insert into author(`username`,`hashed_password`) values ('{}','{}')".format(username,hashed_password)
    print(sql)
    await execute(sql)
    print("创建用户成功")


async def main():
    args = sys.argv[1:]

    command = args[0]
    commands = {
        'create_admin': create_admin
    }

    if command not in commands.keys():
        print('请输入正确的命令')
    await commands[command]()


if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)
