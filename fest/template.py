# -*- coding: utf-8 -*-
import os
import PyV8

try:
    import simplejson as json
except ImportError:
    import json

from django.template import TemplateSyntaxError, TemplateEncodingError
from django.template.loader import get_template
from django.utils.encoding import smart_unicode

from fest.conf import settings


def fest_error(message):
    raise TemplateSyntaxError(message)

class JSError(Exception):
    pass


class TemplateGlobal(PyV8.JSClass):

    def __init__(self, template):
        self.__tpl = template

    def __getattr__(self, name):
        if name == '__fest_error':
            return fest_error

        name = 'py%s' % name
        return PyV8.JSClass.__getattribute__(self, name)

    @property
    def py__dirname(self):
        return settings.FEST_LIB_ROOT

    def py__read_file(self, filename, encoding=None):
        # parts of compiler
        if settings.TEMPLATE_DEBUG:
            return open(filename).read()

        if filename == self.__tpl.template_file:
            template = self.__tpl
        else:
            template = get_template(filename)
        return template.template_string


class Template(object):

    def __init__(self, template_string, template_file=None):
        try:
            template_string = smart_unicode(template_string)
        except UnicodeDecodeError:
            raise TemplateEncodingError('Templates can only be constructed'
                                        ' from unicode or UTF-8 strings.')

        self.template_string = template_string
        self.template_file = template_file

    @property
    def context(self):
        if not hasattr(self, '_context'):
            self._context = PyV8.JSContext(TemplateGlobal(self))
        return self._context

    def compile(self):
        if self.template_file.endswith('.html'):
            return self.template_string

        with self.context as cenv:
            filename = os.path.join(settings.FEST_LIB_ROOT, 'compile.js')
            cenv.eval(open(filename).read())
            return cenv.eval("compile('%s')" % self.template_file)

    def render(self, context):
        if settings.TEMPLATE_DEBUG:
            self.template_string = self.compile()

        if self.template_file.endswith('.html'):
            return self.template_string

        with self.context as cenv:
            template = """
            (function(json_string, fest_error) {
                return %s(JSON.parse(json_string), fest_error);
            })
            """ % self.template_string

            func = cenv.eval(template)
            return func(json.dumps(list(context).pop()), fest_error)

