import os
import sys
import tornado.web
import tornado.options
import aiomysql
import setting


class Application(tornado.web.Application):

    def __init__(self,db):
        self.db = db
        urls = self.get_urls()
        print('urls', urls)
        for url in urls:
            print('http://127.0.0.1:8888'+url[0])
        settings = dict(
            template_path=setting.template_path,
            static_path=setting.static_path,
            debug=setting.debug,
            cookie_secret="lrabbit"

        )
        super().__init__(urls, **settings)

        pass

    def get_urls(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(base_path, 'apps')
        app_urls = []
        for filename in os.listdir('./apps'):
            temp_path = os.path.join(app_path, filename)
            if os.path.isdir(temp_path) and "__pycache__" not in temp_path:
                moudle_name = 'apps.' + filename + '.urls'
                url = getattr(__import__(moudle_name, fromlist=[None]), 'urls')
                app_urls.extend(url)
        return app_urls





async def create_app():

    async with aiomysql.connect(
        host=setting.db_host,
        port=setting.db_port,
        user=setting.db_user,
        password=setting.db_password,
        db=setting.db_database,
        cursorclass=aiomysql.cursors.DictCursor
    ) as db:
        await db.ping()
        application = Application(db)
        return application


if __name__ == '__main__':
    pass
