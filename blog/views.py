# coding=utf-8
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, \
    HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from registration.backends.simple.views import RegistrationView
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from misaka_wrap.md import to_html
from qiniu_wrap.util import get_token
from blog.models import Post, Category
from blog.forms import EditPostForm


def index(request):
    tag = request.GET.get('tag')
    category = request.GET.get('category')
    year = request.GET.get('year')
    month = request.GET.get('month')
    page = request.GET.get('page')
    category_list = Category.objects
    post_list = Post.objects  # Post.objects.order_by('-create_date')
    if tag:
        post_list = post_list.filter(tags__name=tag)
    elif category:
        post_list = post_list.filter(category__name=category)
    elif year and len(year) == 4 and year.isdigit():
        post_list = Post.objects.filter(create_date__year=year)
    elif month and 4 < len(month) < 7 and month.isdigit():
        post_list = post_list.filter(create_date__year=month[:4],
                                     create_date__month=month[4:])

    paginator = Paginator(post_list.order_by('-create_date'), 7)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
                'posts': posts,
                'category_list': category_list
            }
    return render(request, 'blog/index.html', context)


def single_post(request, post_title):
    post = get_object_or_404(Post, title=post_title)
    if post.is_hide and not request.user.is_authenticated():
        return HttpResponseNotFound()
    return render(request, 'blog/single_post.html', {'post': post})


@login_required()
def new_post(request):
    if request.method == 'POST':
        form = EditPostForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            return redirect('blog:single_post', post_title=new.title)
    else:
        form = EditPostForm()
    return render(request,
                  'blog/edit_post.html',
                  {
                    'title': u'新文章',
                    'form': form,
                  })


@login_required()
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = EditPostForm(data=request.POST, instance=post)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            form.save_m2m()
            return redirect('blog:single_post', post_title=post.title)
    else:
        form = EditPostForm(instance=post)
    return render(request,
                  'blog/edit_post.html',
                  {
                    'post': post,
                    'title': u'编辑 - ' + post.title,
                    'form': form,
                  })


@login_required()
def create_category(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST['name']
        if name:
            row, _ = Category.objects.get_or_create(name=name)
            return JsonResponse({'pk': row.id})


@login_required()
def preview_post(request):
    if request.method == 'POST' and request.is_ajax():
        return JsonResponse({'html': to_html(request.POST['md'])})


@login_required()
def generate_qiniu_token(request):
    return JsonResponse({'uptoken': get_token()})


@login_required()
def generate_qiniu_key(request):
    return JsonResponse({'key': uuid.uuid4().hex})


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/blog/'
