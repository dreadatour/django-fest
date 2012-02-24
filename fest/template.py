# -*- coding: utf-8 -*-
import os
import PyV8

try:
    import simplejson as json
except ImportError:
    import json

from django.template import TemplateEncodingError
from django.template.loader import get_template
from django.utils.encoding import smart_unicode

from fest.conf import settings


class JSLocker(PyV8.JSLocker):
    def __enter__(self):
        self.enter()

        if JSContext.entered:
            self.leave()
            raise RuntimeError("Lock should be acquired before enter the context")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if JSContext.entered:
            self.leave()
            raise RuntimeError("Lock should be released after leave the context")

        self.leave()

    def __nonzero__(self):
        return self.entered()


class JSContext(PyV8.JSContext):
    def __init__(self, obj=None, extensions=None, ctxt=None):
        if JSLocker.active:
            self.lock = JSLocker()
            self.lock.enter()

        if ctxt:
            PyV8.JSContext.__init__(self, ctxt)
        else:
            PyV8.JSContext.__init__(self, obj, extensions or [])

    def __enter__(self):
        self.enter()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.leave()

        if hasattr(JSLocker, 'lock'):
            self.lock.leave()
            self.lock = None

        del self


class JSError(Exception):
    pass


def fest_error(message):
    raise JSError(message)


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
        filename = os.path.normpath(filename)
        if settings.TEMPLATE_DEBUG:
            return open(filename).read()

        if filename == self.__tpl.template_file:
            template = self.__tpl
        else:
            template = get_template(filename)
        return template.template_string


class Template(object):

    def __init__(self, template_string, template_file=None, template_name=None):
        try:
            template_string = smart_unicode(template_string)
        except UnicodeDecodeError:
            raise TemplateEncodingError('Templates can only be constructed'
                                        ' from unicode or UTF-8 strings.')

        if template_name is not None:
            template_name = os.path.normpath(template_name)
            if template_name.endswith('.xml'):
                template_name = "__fest__template__%s" % template_name[:-4].replace('/', '_')
            elif template_name.endswith('.js'):
                template_name = "__fest__template__%s" % template_name[:-3].replace('/', '_')
            else:
                template_name = None

        self.template_string = template_string
        self.template_file = template_file
        self.template_name = template_name

    @property
    def context(self):
        if not hasattr(self, '_context'):
            self._context = JSContext(TemplateGlobal(self))
        return self._context

    @property
    def template(self):
        if not hasattr(self, '_template'):
            with self.context as cenv:
                cenv.eval("""
                    var %s = (function(json_string, fest_error) {
                        return %s(JSON.parse(json_string), fest_error);
                    })
                """ % (self.template_name, self.template_string))
            self._template = self.template_name
        return self._template


    def compile(self):
        if self.template_file.endswith('.html'):
            return self.template_string

        with self.context as cenv:
            filename = os.path.join(settings.FEST_LIB_ROOT, 'compile.js')
            cenv.eval(open(filename).read())
            self.template_string = cenv.eval("compile('%s')" % self.template_file)

    def render(self, context):
        if self.template_file.endswith('.html'):
            return self.template_string

        with JSLocker():
            if settings.TEMPLATE_DEBUG:
                self.compile()

            with self.context as cenv:
                func = cenv.eval(self.template)
                return func(json.dumps(list(context).pop()), fest_error)

