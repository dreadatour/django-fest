# -*- coding: utf-8 -*-
import os

from django.conf import settings


settings.FEST_ROOT = os.path.normpath(getattr(settings, 'FEST_ROOT',
        os.path.join(settings.STATIC_ROOT, 'fest')))

settings.FEST_LIB_ROOT = os.path.normpath(getattr(settings, 'FEST_LIB_ROOT',
        os.path.join(settings.FEST_ROOT, 'lib')))

settings.FEST_TEMPLATES_ROOT = os.path.normpath(getattr(settings, 'FEST_TEMPLATES_ROOT',
        os.path.join(settings.FEST_ROOT, 'templates')))

