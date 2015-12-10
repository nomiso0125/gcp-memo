#!-*- coding:utf-8 -*-


from datetime import date
from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import search
from lib.controller import *
from models.user_model import UserModel


# テストデータ作成
UserModel(id="user1", user_name=u"鈴木 一郎", height=172, birthday=date(1980, 1, 1)).put()
UserModel(id="user2", user_name=u"田中 太郎", height=168, birthday=date(1977, 5, 23)).put()
UserModel(id="user3", user_name=u"佐藤 花子", height=158, birthday=date(2001, 12, 10)).put()


class Top(Controller):
    def post(self):
        self.get()

    def get(self):

        # ------------------------------------------
        # ユーザー1の情報を得る
        # ------------------------------------------
        user1 = UserModel.get_by_id('user1')
        self.set_template_value('user1', user1)

        # ------------------------------------------
        # Search API検索
        # ------------------------------------------
        user_name = self.request.get('user_name')
        height = self.request.get('height')
        birthday1 = self.request.get('birthday1')
        birthday2 = self.request.get('birthday2')

        queries = list()
        if user_name:
            queries.append(u"user_name = {0}".format(user_name))
        if height:
            queries.append(u"height = {0}".format(height))
        if birthday1:
            queries.append(u"birthday >= {0}".format(birthday1))
        if birthday2:
            queries.append(u"birthday <= {0}".format(birthday2))

        query = ''
        if queries:
            query = ' AND '.join(queries)

        index = search.Index('UserIndex')
        results = index.search(query)

        self.set_template_value('results', results)

        self.draw_template('front/search_api/top.html')


        return


class Save(Controller):

    def post(self):

        # ユーザーデータの保存
        self.save_user()

        self.redirect('/search_api/top')

        return

    @ndb.transactional()
    def save_user(self):

        user_name = self.request.get('user_name')
        height = self.request.get('height')
        birthday = self.request.get('birthday')
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

        user1 = UserModel.get_by_id('user1')
        user1.user_name = user_name
        user1.height = int(height)
        user1.birthday = birthday
        user1.put()

        # raise Exception


url_map = [
    ('/search_api/top', Top),
    ('/search_api/save', Save),
]

application = webapp.WSGIApplication(url_map, debug=True)
