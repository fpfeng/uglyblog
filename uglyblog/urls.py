"""uglyblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from blog.views import MyRegistrationView
from blog.forms import NewRegisterForm, LoginForm


urlpatterns = [
    url(r'^blog/captcha/', include('captcha.urls')),
    url(r'^blog/accounts/register/$',
        MyRegistrationView.as_view(disallowed_url='/blog/',
                                   form_class=NewRegisterForm),
        name='registration_register'),
    url(r'^blog/accounts/login/$',
        login,
        {'authentication_form': LoginForm},
        name='login'),
    url(r'^blog/accounts/logout/$', logout, {'next_page': '/blog/'}, name='logout'),
    url(r'^blog/accounts/', include('registration.backends.simple.urls')),
    url(r'^blog/admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
]
