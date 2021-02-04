from .api import *

urls = [
    (r'/chat', IndexHandle),
    (r'/chatsocket', ChatSocketHandler)
]
