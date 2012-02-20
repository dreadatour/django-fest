# -*- coding: utf-8 -*-
import os

from django.template.base import TemplateDoesNotExist
from django.template.loaders import app_directories, filesystem

from fest.conf import settings
from fest.template import Template


class FSLoader(filesystem.Loader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        return Template(source, origin), origin

    def load_template_source(self, template_name, template_dirs=None):
        if settings.TEMPLATE_DEBUG or template_name.endswith('.html'):
            return super(FSLoader, self).load_template_source(template_name, template_dirs)

        filepath = os.path.join(settings.FEST_TEMPLATES_ROOT, template_name)
        if filepath.endswith('.xml'):
            filepath = '%s.js' % filepath[:-4]

        try:
            file = open(filepath)
            try:
                return (file.read().decode(settings.FILE_CHARSET), filepath)
            finally:
                file.close()
        except IOError:
            raise TemplateDoesNotExist('Template %s not found.' % filepath)

