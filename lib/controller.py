#!-*- coding:utf-8 -*-

import os

import webapp2 as webapp
import jinja2

#------------------------------------------
# Template Cache
#------------------------------------------
template_cache = dict()

#------------------------------------------
# Template Settings
#------------------------------------------
template_path = os.path.join(os.getcwd(), 'templates/')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path),
    cache_size=-1
)


class Controller(webapp.RequestHandler):
    def __init__(self, request=None, response=None):

        webapp.RequestHandler.__init__(self, request=request, response=response)

        self.template_values = {}

    def set_template_value(self, key, value):

        self.template_values[key] = value
        return

    def set_template_values(self, values):

        self.template_values.update(values)
        return

    def is_local(self):

        if os.environ['HTTP_HOST'].startswith('localhost'):
            return True
        else:
            return False

    def get_render_html(self, path, encode=''):

        arguments = self.request.arguments()

        for argument in arguments:
            self.set_template_value(argument, self.request.get(argument))

        # Use Template Cache
        if self.is_local():
            template = jinja_environment.get_template(path)
        else:
            template = template_cache.get(path)
            if not template:
                template = jinja_environment.get_template(path)
                template_cache[path] = template

        self.set_template_value('request_path', self.request.path)

        html = template.render(self.template_values)

        if encode:
            html = html.encode(encode)

        return html

    def draw_template(self, path, encode='', content_type="application/xhtml+xml"):

        html = self.get_render_html(path, encode=encode)

        self.response.out.write(html)

        return
