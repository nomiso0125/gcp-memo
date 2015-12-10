#!-*- coding:utf-8 -*-

from google.appengine.api import search
from google.appengine.ext import ndb
from google.appengine.ext import deferred


class UserModel(ndb.Model):
    """
    ユーザーモデル
    """
    user_name = ndb.StringProperty()        # 名前
    height = ndb.IntegerProperty()          # 身長
    birthday = ndb.DateProperty()           # 誕生日

    @classmethod
    def put_search_document(cls, key_id):
        model = ndb.Key(cls, key_id).get()
        if model:
            document = search.Document(
                doc_id=key_id,
                fields=[
                    search.TextField(name='user_name', value=model.user_name),
                    search.NumberField(name='height', value=model.height),
                    search.DateField(name='birthday', value=model.birthday),
                   ])
            index = search.Index(name="UserIndex")
            index.put(document)

    def _post_put_hook(self, future):
        deferred.defer(UserModel.put_search_document,
                       self.key.id(),
                       _transactional=ndb.in_transaction())
