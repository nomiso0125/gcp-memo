#!-*- coding:utf-8 -*-
#!/usr/bin/env python

from lib.controller import *
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

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

class Movie(Controller):
    def get(self):
        self.draw_template('front/member/movie.html')


class PlayMovie(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):

        blob_key = blobstore.create_gs_key('/gs/gcp-memo.appspot.com/movies/meteorite.mp4')

        self.send_blob(blob_key)

url_map = [
    ('/member/top', Top),
    ('/member/movie', Movie),
    ('/member/play_movie', PlayMovie),
]

application = webapp.WSGIApplication(url_map, debug=True)
