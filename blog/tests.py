# coding: utf-8
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User, Permission
from .models import Category, Post


class BaseSetup(TestCase):
    def setUp(self):
        super(BaseSetup, self).setUp()
        self.username = 'testuser'
        self.password = 'testpassword'

    def get_conf(self, name):
        return getattr(settings, name, '')

    def add_user(self):
        self.client.post(
                    reverse('registration_register'),
                    {
                        'username': self.username,
                        'password1': self.password,
                        'password2': self.password,
                        'email': 'test@exmaple.com',
                        })

    def login(self):
        self.client.post(reverse('login'),
                         {
                            'username': self.username,
                            'password': self.password,
                        })

    def logout(self):
        self.client.get(reverse('logout'))

    def post_create_category(self, name):
        resp = self.client.post(reverse('blog:create_category'),
                                {
                                    'name': name
                                },
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest',)
        self.assertContains(resp, 'pk')

    def get_category_id(self, index=0):
        return Category.objects.all()[index].id

    def post_new_post(self, title, content, tags, cat=None):
        if not cat:
            cat = self.get_category_id()
        self.client.post(reverse('blog:new_post'),
                         {
                            'title': title,
                            'subtitle': u'testsubtitle副标题💪',
                            'content': content * 10,
                            'category': cat,
                            'header_image_url': 'http://exmaple.com/t.jpg',
                            'tags': tags,
                            'is_hide': 0
                         }, follow=True)

    def post_edit_post(self, url, tags, title, content, hide=0):
        self.client.post(url,
                         {
                            'title': title,
                            'subtitle': u'testsubtitle副标题💪',
                            'content': content * 10,
                            'category': self.get_category_id(),
                            'header_image_url': 'http://exmaple.com/q.jpg',
                            'tags': tags,
                            'is_hide': hide
                         }, follow=True)

    def get_post_url(self, title):
        return reverse('blog:single_post', kwargs={'post_title': title})

    def get_index(self):
        return self.client.get(reverse('blog:index'))


class TestAjaxApi(BaseSetup):

    def test_create_category(self):
        self.add_user()
        self.login()

        cat_name = 'testcategory'
        self.post_create_category(cat_name)

        resp = self.client.get(reverse('blog:index'))
        self.assertContains(resp, cat_name)

    def test_preview_post(self):
        self.add_user()
        self.login()

        post_content = 'testpostcontent'
        resp = self.client.post(reverse('blog:preview_post'),
                                {
                                    'md': post_content
                                },
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(resp, post_content)

    def test_qiniu_token(self):
        self.add_user()
        self.login()

        resp = self.client.get(reverse('blog:gen_qtoken'))
        self.assertContains(resp, 'uptoken')

    def test_qiniu_key(self):
        self.add_user()
        self.login()

        resp = self.client.get(reverse('blog:gen_qkey'))
        self.assertContains(resp, 'key')


class TestView(BaseSetup):

    def test_none_post_index(self):
        resp = self.client.get(reverse('blog:index'))
        self.assertContains(resp, u'没找到符合的文章')

    def test_filter(self):
        text = u'没找到符合的文章'
        resp = self.client.get(reverse('blog:index') + '?tag=none')
        self.assertContains(resp, text)

        resp = self.client.get(reverse('blog:index') + '?year=1999')
        self.assertContains(resp, text)

        resp = self.client.get(reverse('blog:index') + '?month=1')
        self.assertContains(resp, text)

    def test_register_page(self):
        resp = self.client.get(reverse('registration_register'))
        self.assertContains(resp, u'用户名')

    def test_register_login_logout(self):
        # not login
        resp = self.client.get(reverse('blog:new_post'), follow=True)
        self.assertContains(resp, u'登录')
        resp = self.client.post(
                                reverse('registration_register'),
                                {
                                    'username': 'testuser',
                                    'password1': 'testpassword',
                                    'password2': 'testpassword',
                                    'email': 'test@exmaple.com',
                                })
        self.assertTrue(resp.status_code, 200)
        # after login
        resp = self.client.get(reverse('blog:index'))
        self.assertNotContains(resp, u'登录')
        # after logout
        self.logout()
        resp = self.client.get(reverse('blog:index'))
        self.assertContains(resp, u'登录')

    def test_new_post_index(self):
        self.add_user()
        self.login()
        resp = self.client.get(reverse('blog:new_post'))
        self.assertContains(resp, u'新文章')

    def test_all_about_post(self):
        self.add_user()
        self.login()

        cat_name = u'新分类😱new'
        tags = u'标签, tag1'
        post_title = u'测试标题    ！testtitle😙'
        content = u'test中文😐content1《）内容'
        self.post_create_category(cat_name)
        self.post_new_post(post_title, content, tags)
        # new post in index
        resp = self.client.get(reverse('blog:index'))
        self.assertContains(resp, cat_name)
        self.assertContains(resp, u'>标签<')
        self.assertContains(resp, '>tag1<')
        self.assertContains(resp, post_title)
        url = self.get_post_url(post_title)
        # single post page
        resp = self.client.get(url)
        self.assertContains(resp, content)

        new_cat = u'new分类😱'
        new_tag = u'新标签, new'
        new_title = 'new~~~标题 😙'
        new_content = 'new~~~😐《）内容'
        hide_post = 1
        self.post_create_category(new_cat)
        edit_url = reverse('blog:edit_post',
                           kwargs={'post_id': Post.objects.all()[0].id})
        self.post_edit_post(edit_url, new_tag, new_title, new_content, hide_post)
        url = self.get_post_url(new_title)
        resp = self.client.get(url)
        self.assertContains(resp, new_content)
        self.assertContains(resp, u'>新标签<')
        self.assertContains(resp, u'>new<')

        month = datetime.now().month
        resp = self.get_index()
        self.assertContains(resp, new_cat)
        self.assertContains(resp, u'{0}月 (1)'.format(month))
        self.assertContains(resp, u'>新标签<')
        self.assertContains(resp, u'>new<')

        # hide from not login user
        self.logout()
        resp = self.get_index()
        self.assertNotContains(resp, new_title)
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)

    def test_posts_filter(self):
        self.add_user()
        self.login()

        cat1 = 'cat1'
        cat2 = 'cat2'
        self.post_create_category(cat1)
        self.post_create_category(cat2)

        title1 = 'title1'
        title2 = 'title2'
        content1 = 'content1'
        content2 = 'content2'
        tag1 = 'tag1'
        tag2 = 'tag2'
        cat1_id = self.get_category_id()
        cat2_id = self.get_category_id(1)
        self.post_new_post(title1, content1, tag1, cat=cat1_id)
        self.post_new_post(title2, content2, tag2, cat=cat2_id)

        month = datetime.now().month
        year = datetime.now().year

        p2 = Post.objects.all()[1]

        new_date = p2.create_date.replace(year=2015).replace(month=1)
        p2.create_date = new_date
        p2.save()
        resp = self.get_index()
        self.assertContains(resp, '2015')
        self.assertContains(resp, '2016')
        self.assertContains(resp, u'{0}月 (1)'.format(month))
        self.assertContains(resp, u'1月 (1)')

        resp = self.client.get(reverse('blog:index') + '?tag={0}'.format(tag1))
        self.assertContains(resp, title1)
        self.assertNotContains(resp, title2)

        resp = self.client.get(reverse('blog:index') + '?year=2015')
        self.assertContains(resp, title2)
        self.assertNotContains(resp, title1)

        p1 = Post.objects.all()[0]
        resp = self.client.get(reverse('blog:index') + '?month={0}{1}'.format(year, month))
        self.assertContains(resp, p1.title)
        self.assertNotContains(resp, p2.title)

    def test_register_close(self):
        with self.settings(REGISTRATION_OPEN=False):
            resp = self.client.get(reverse('registration_register'), follow=True)
            self.assertNotContains(resp, u'再次输入密码')

    def test_refresh_captcha(self):
        resp = self.client.get(reverse('captcha-refresh'),
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(resp, 'key')
        self.assertContains(resp, 'image_url')
