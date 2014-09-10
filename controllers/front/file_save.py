#!-*- coding:utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import app_identity
from lib.controller import *
import lib.cloudstorage as gcs
from models.user_file_model import UserFileModel


class Top(Controller):
    def get(self):
        upload_url = blobstore.create_upload_url('/file_save/upload2')

        self.set_template_value('upload_url', upload_url)
        self.draw_template('front/file_save/top.html')


class Upload1(Controller):
    def post(self):

        file_data = self.request.get('file_data')

        user_file = UserFileModel()
        user_file.file_data = file_data
        user_file.put()

        self.set_template_value('message', str(user_file.key))
        self.draw_template('front/file_save/done.html')


class Upload2(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):

        upload_files = self.get_uploads('file_data')

        blob_info = upload_files[0]

        self.redirect('/file_save/upload2_done?key=%s' % blob_info.key())


class Upload2Done(Controller):
    def get(self):

        key = self.request.get('key')

        self.set_template_value('message', key)
        self.draw_template('front/file_save/done.html')


class Upload3(Controller):
    def post(self):

        # ファイル名とファイルデータを得る
        file_name = self.request.POST['file_data'].filename
        file_data = self.request.get('file_data')

        # このアプリケーションのGCSバケット名を得る
        bucket_name = app_identity.get_default_gcs_bucket_name()

        # 保存パスを作成
        filepath = '/' + bucket_name + '/file_save/' + file_name

        # ファイル作成
        gcs_file = gcs.open(filepath, 'w')
        gcs_file.write(file_data)
        gcs_file.close()

        gcs_key = blobstore.create_gs_key('/gs' + filepath)

        self.set_template_value('message', gcs_key)
        self.draw_template('front/file_save/done.html')

url_map = [
    ('/file_save/top', Top),
    ('/file_save/upload1', Upload1),
    ('/file_save/upload2', Upload2),
    ('/file_save/upload2_done', Upload2Done),
    ('/file_save/upload3', Upload3),

]

application = webapp.WSGIApplication(url_map, debug=True)
