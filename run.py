import tornado
from tornado.options import options
from make_app import create_app
import tornado.locks
import tornado.ioloop

from tornado.options import options
from tornado.options import define
import tornado.log

define('port', default=8888, type=int)
define('address', default='127.0.0.1')


async def main():
    tornado.options.parse_command_line()
    app = await create_app()
    app.listen(options.port, options.address)
    print('http://127.0.0.1:' + str(options.port))
    shutDown = tornado.locks.Event()
    await shutDown.wait()

if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)
