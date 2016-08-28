# coding=utf-8
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from taggit.forms import TagWidget
from registration.forms import RegistrationForm
from captcha.fields import CaptchaField
from blog.models import Post


UserModel = get_user_model


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()

    class Meta:
        fields = ['username', 'password', 'captcha']


class NewRegisterForm(RegistrationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        names = {
            'username': u'用户名',
            'email': u'邮箱地址',
            'password1': u'密码',
            'password2': u'再次输入密码 确认无误',
        }

        for k in self.fields.keys():
            self.fields[k].label = ''
            self.fields[k].help_text = ''
            self.fields[k].widget.attrs['class'] = 'form-control'
            self.fields[k].widget.attrs['placeholder'] = names[k]


class EditPostForm(ModelForm):

    class Meta:
        model = Post
        fields = [
                  'category',
                  'tags',
                  'title',
                  'subtitle',
                  'header_image_url',
                  'content',
                  'is_hide',
                  ]
        widgets = {
            'title': TextInput(attrs={
                               'placeholder': u'标题',
                               'class': 'form-control'}),
            'subtitle': TextInput(attrs={
                                   'placeholder': u'副标题',
                                   'class': 'form-control'}),
            'tags': TagWidget(attrs={
                              'placeholder': u'使用分号 ; 逗号 , 分隔',
                              'class': 'tag-real-input'}),
            'header_image_url': TextInput(attrs={
                                          'id': 'bg-image-url',
                                          'class': 'form-control',
                                          'placeholder': u'文章头版背景图',
                                          'readonly': ''}),
            'content': Textarea(attrs={
                                'placeholder': u'正文',
                                'rows': 25,
                                }),
            'is_hide': CheckboxInput(attrs={
                                     'value': 0
                                     })
            }
