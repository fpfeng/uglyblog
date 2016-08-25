# uglyblog

学习 django 项目，一个简单的博客。     
和主题 [clean blog](https://startbootstrap.com/template-overviews/clean-blog/) 紧密结合，文章`header`图片在编辑页面上传，其他页面按照`django url name`命名读取七牛图片。

## 已有功能
用户的登录注册，使用 [django-registration](https://github.com/ubernostrum/django-registration/)       
登录验证码，使用 [django-simple-captcha](https://github.com/mbi/django-simple-captcha)         
文章的多标签，使用 [django-taggit](https://github.com/alex/django-taggit)     
markdown 支持，使用 [misaka](https://github.com/FSX/misaka)      
代码高亮，使用 [highlight.js](https://highlightjs.org/)  
在线预览编辑文章，jquery ajax + misaka    
七牛保存文章的图片附件，纯前端上传         
文章页自动生成目录，使用 [bootstrap-toc](https://github.com/afeld/bootstrap-toc)      

## 测试运行
git clone     
安装依赖包     
改名`uglybog/test_settings.py`，修改`mysql`参数     
跑一遍单元测试    
```bash                                                                  
export DJANGO_SETTINGS_MODULE="uglyblog.test_settings"             
./manage.py test blog                                                          
```
 无误，`uglybog/dev_settings.py`同上并修改七牛参数，生成假数据
```bash  
export DJANGO_SETTINGS_MODULE="uglyblog.dev_settings"                  
./manage.py makemigrations blog          
./manage.py migrate       
./manage.py fake_site       
./manage.py runserver            
```
