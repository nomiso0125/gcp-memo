#!-*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from lib.controller import *
from google.appengine.api import users


class Warmup(Controller):
    def get(self):
        logging.info('warm up done.')


class Xrds(Controller):
    def get(self):
        self.draw_template('front/system/xrds.xml')


class LoginRequired(Controller):
    def get(self):

        # 各OpenIDプロバイダのログインURLを得る
        mixi_url = users.create_login_url(dest_url='/member/top', federated_identity='https://mixi.jp/')
        self.set_template_value('mixi_url', mixi_url)

        google_url = users.create_login_url(dest_url='/member/top', federated_identity='https://www.google.com/accounts/o8/id')
        self.set_template_value('google_url', google_url)

        docomo_url = users.create_login_url(dest_url='/member/top', federated_identity='https://i.mydocomo.com')
        self.set_template_value('docomo_url', docomo_url)

        softbank_url = users.create_login_url(dest_url='/member/top', federated_identity='https://id.my.softbank.jp/')
        self.set_template_value('softbank_url', softbank_url)

        self.draw_template('front/system/login_required.html')

#-------------------------------------------------
# URLマッピング
#-------------------------------------------------
url_map = [
    ('/_ah/warmup', Warmup),
    ('/_ah/xrds', Xrds),
    ('/_ah/login_required', LoginRequired),
]

application = webapp.WSGIApplication(url_map, debug=True)
