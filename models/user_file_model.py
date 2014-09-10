#!-*- coding:utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import ndb


class UserFileModel(ndb.Model):
    """
    ファイル格納モデル
    """
    file_data = ndb.BlobProperty()                  # ファイルデータ
