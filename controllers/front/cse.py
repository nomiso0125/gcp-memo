#!-*- coding:utf-8 -*-
#!/usr/bin/env python

import json
import logging
import urllib
from google.appengine.api import urlfetch
from lib.controller import *


class Top(Controller):
    def get(self):
        self.draw_template('front/cse/top.html')


class Search(Controller):
    def post(self):

        # キーワードを得る
        keyword = self.request.get('keyword')

        # 評価が指定されていればキーワードに追加
        stars = self.request.get('stars')
        if stars:
            keyword += ' ' + 'more:pagemap:review-ratingstars:%s' % stars

        # urlエンコード
        keyword = urllib.quote(keyword.encode('utf-8'))

        # リクエストパラメータ組み立て
        url = 'https://www.googleapis.com/customsearch/v1'
        url += '?key=%s' % 'YOUR_API_KEY'
        url += '&cx=%s' % '000122034385005128488:etmrnaufuww'
        url += '&q=%s' % keyword

        # 検索
        result = urlfetch.fetch(url)

        logging.info(url)

        items = list()
        if not 200 <= result.status_code <= 299:
            # エラー
            logging.error('google custom search error: %s' % str(result.status_code))
            logging.error(result.content)
        else:
            # 結果を得る
            content_dict = json.loads(result.content)
            items = content_dict.get('items', list())

        self.set_template_value('items', items)
        self.draw_template('front/cse/search.html')


url_map = [
    ('/cse/top', Top),
    ('/cse/search', Search),
]

application = webapp.WSGIApplication(url_map, debug=True)
