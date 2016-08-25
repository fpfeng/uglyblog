from __future__ import unicode_literals

from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'BlogConfig'

    # def ready(self):
    #     import blog.signals.handlers
    #     pass
