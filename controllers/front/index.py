#!-*- coding:utf-8 -*-
#!/usr/bin/env python


from lib.controller import *
from google.appengine.api import users


class Top(Controller):
    def get(self):

        self.draw_template('front/index.html')


url_map = [
    ('/', Top),
]

application = webapp.WSGIApplication(url_map, debug=True)
