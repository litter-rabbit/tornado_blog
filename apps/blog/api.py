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
        page_size = setting.page_size
        sql = "select * from article limit {} offset {}".format(page_size, 0)
        articles = await self.query(sql)
        self.render('blog/index.html', articles=articles)

    async def patch(self):
        data = self.get_json_body(self.request.body)
        page = data['page']
        page_size = setting.page_size
        sql = "select * from article limit {} offset {}".format(page_size, (page - 1) * page_size)
        articles = await self.query(sql)
        self.write({"articles": articles})


class LoginHandler(BaseHandler):

    async def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        sql = "select * from author where username='{}'".format(username)
        print(sql)
        author = await self.query_one(sql)
        if not author:
            self.redirect('/')

        password_equal = await tornado.ioloop.IOLoop.current().run_in_executor(
            None,
            bcrypt.checkpw,
            tornado.escape.utf8(password),
            tornado.escape.utf8(author['hashed_password'])
        )
        if password_equal:
            print('clear')
            self.set_secure_cookie('current_user', tornado.escape.to_unicode(str(author['id'])))
            self.redirect('/')
        else:
            self.redirect('/')


class ManagePostHandler(BaseHandler):

    async def get(self):
        page = self.get_argument('page', 1)
        page_size = setting.page_size
        sql = "select * from article limit {} offset {}".format(page_size, (page - 1) * page_size)
        articles = await self.query(sql)
        self.render('blog/post_manage.html', articles=articles)

    async def delete(self):
        data = self.get_json_body(self.request.body)
        id = data['id']
        sql = "delete from article where id={}".format(id)
        await self.execute(sql)
        self.set_header('Request Method', 'GET')


class DetailArticle(BaseHandler):

    async def get(self):
        id = self.get_argument('id')
        sql = "select * from article where id='{}'".format(id)
        article = await self.query_one(sql)
        if article:
            self.render('blog/post_detail.html', article=article)
        else:
            self.render('error/404.html', message="文章未找到")


class PostArticle(BaseHandler):

    async def get(self):

        id = self.get_escape_argument('id')
        article = None
        if id:
            sql = "select * from article where id='{}'".format(id)
            article = await self.query_one(sql)

        self.render('blog/post_article.html', article=article)

    def put(self):
        data = self.get_json_body(self.request.body)
        text = data['text']
        html = markdown.markdown(text)
        print(html)
        self.write({'html': html})

    async def post(self):
        id = self.get_argument('article_id', None)
        raw_text = self.get_argument("text")
        text = self.get_escape_argument('text')
        title = self.get_escape_argument('title')
        html = markdown.markdown(raw_text, extensions=['markdown.extensions.toc', 'markdown.extensions.fenced_code'])
        html = aiomysql.escape_string(html)
        print(html)
        if id:
            sql = "select count(*) from as count article where id='{}'".format(id)
            result = self.query(sql)
            if result[0]['count'] > 0:
                sql = "update article set title='{}',text='{}',html='{}',updated='{}' where id={}".format(
                    title, text, html, self.get_format_time(),
                )
                self.execute(sql)

        else:
            sql = "insert into article(`title`,`text`,`html`,`published`,`updated`,`is_published`) values('{}','{}','{}','{}','{}','{}')".format(

                title, text, html, self.get_format_time(), self.get_format_time(), '1'
            )
            print(sql)
            await self.execute(sql)

        self.redirect('/')
