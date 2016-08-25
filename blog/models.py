# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager
from django.utils.html import strip_tags
from misaka_wrap.md import to_html


class Category(models.Model):
    name = models.CharField(max_length=20)

    class meta:
        db_table = 'category'

    def __unicode__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    header_image_url = models.CharField(max_length=100, blank=True)
    tags = TaggableManager()
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    content = models.TextField()
    content_html = models.TextField()
    content_summary = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    is_hide = models.BooleanField(default=False)

    class meta:
        db_table = 'post'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
            if self.content:
                self.content_html = to_html(self.content)
                self.content_summary = strip_tags(self.content_html[:220])[:180]
            super(Post, self).save(*args, **kwargs)
