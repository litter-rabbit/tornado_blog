from .api import *

urls = [(r'/get_tasks', IndexHandler),
        (r'/post_tasks', SubmitTask),
        (r'/push_response',PushResponse)
        ]
