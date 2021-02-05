

from ..baseHandler import  BaseHandler


class IndexHandle(BaseHandler):


    def get(self):
        self.render('tools/index.html')
