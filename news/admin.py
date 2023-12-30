from django.contrib import admin
from .models import Category, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug'
    ]



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'body', 'publish', 'image', 'status'
    ]
    list_filter = [
        'status', 'publish'
    ]
    search_fields = ['title', 'body']
