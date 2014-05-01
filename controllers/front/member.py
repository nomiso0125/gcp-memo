#!-*- coding:utf-8 -*-
#!/usr/bin/env python


from lib.controller import *
from google.appengine.api import users


class Top(Controller):
    def get(self):

        # ニックネームを得る
        user = users.get_current_user()
        nickname = user.nickname()
        self.set_template_value('nickname', nickname)

        # ログアウトURLを得る
        logout_url = users.create_logout_url('/')
        self.set_template_value('logout_url', logout_url)

        self.draw_template('front/member/top.html')


url_map = [
    ('/member/top', Top),
]

application = webapp.WSGIApplication(url_map, debug=True)
