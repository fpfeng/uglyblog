from django.contrib import admin
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('create_date',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
