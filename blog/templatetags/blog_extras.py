from django import template
from django.conf import settings
from blog.models import Post, Category


register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag
def app_conf(name):
    return getattr(settings, name, '')


@register.simple_tag
def open_register():
    return settings.REGISTRATION_OPEN


@register.simple_tag
def header_image_url(url_name):
    base = settings.QINIU_BASE_URL
    return base + 'image/header-bg/' + url_name + '.jpg'


@register.inclusion_tag('blog/snippets/form_wrap_div.html')
def wrap_div(form, div_class='', form_class='', placeholder=''):
    if not form_class:
        form_class = 'form-control'
    if not div_class:
        div_class = 'form-group'
    return {
            'form': form,
            'div_class': div_class,
            'form_class': form_class,
            'placeholder': placeholder,
            }


@register.inclusion_tag('blog/snippets/post_archive.html')
def post_archive():
    return {'post_list': Post.objects.order_by('-create_date')}


@register.inclusion_tag('blog/snippets/category_archive.html')
def category_archive():
    return {'category_list': Category.objects}
