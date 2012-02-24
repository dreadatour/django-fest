# -*- coding: utf-8 -*-
import os
from fnmatch import fnmatch

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.template import TemplateDoesNotExist
from django.template.loader import find_template
from django.template.loaders.cached import Loader as CachedLoader
from django.test.utils import override_settings

from fest.template import Template


class Command(NoArgsCommand):

    @override_settings(TEMPLATE_DEBUG=True)
    def handle_noargs(self, **options):
        # Force django to calculate template_source_loaders
        try:
            find_template('notexists')
        except TemplateDoesNotExist:
            pass

        from django.template.loader import template_source_loaders

        loaders = []
        for loader in template_source_loaders:
            if isinstance(loader, CachedLoader):
                loaders.extend(loader.loaders)
            else:
                loaders.append(loader)

        paths = set()
        for loader in loaders:
            paths.update(list(loader.get_template_sources('')))

        templates = list()
        for path in paths:
            for root, dirs, files in os.walk(path):
                for name in files:
                    if not name.startswith(('.', '_')) and name.endswith('.xml'):
                        templates.append(dict({
                            'root': path,
                            'file': os.path.join(root[len(path)+1:], name)
                        }))

        storage = FileSystemStorage(settings.FEST_TEMPLATES_ROOT)
        print "Compile templates:"
        for template in templates:
            template_file = os.path.join(template['root'], template['file'])
            filename = template['file']

            content = open(template_file)
            try:
                tpl = Template(content.read().decode(settings.FILE_CHARSET),
                               template_file=template_file,
                               template_name=filename)
                tpl.compile()
                compiled = ContentFile(tpl.template_string)
            finally:
                content.close()

            filename = '%s.js' % filename[:-4]
            print "%s -> %s" % (template['file'], filename)

            storage.delete(filename)
            storage.save(filename, compiled)

