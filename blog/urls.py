from django.conf.urls import url, include
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/', views.new_post, name='new_post'),
    url(r'^ajax_category/', views.create_category, name='create_category'),
    url(r'^preview_post/', views.preview_post, name='preview_post'),
    url(r'^gen_qtoken/', views.generate_qiniu_token, name='gen_qtoken'),
    url(r'^gen_qkey/', views.generate_qiniu_key, name='gen_qkey'),
    url(r'^(?P<post_title>[^/]+)/$', views.single_post, name='single_post'),
    url(r'^(?P<post_id>[0-9]+)/edit/$', views.edit_post, name='edit_post'),
]
