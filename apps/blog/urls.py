from .api import *

urls = [(r'/', IndexHandler),
        (r'/post_article/[^/]*',PostArticle),
        (r'/post_article',PostArticle),
        (r'/manage_article',ManagePostHandler),
        (r'/manage_article/[^/]*',ManagePostHandler),
        (r'/post_detail/[^/]*',DetailArticle),
        (r'/login',LoginHandler),
        (r'/closed',ClosedHandler)
        ]
