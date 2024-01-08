from django.contrib import admin

from .models import Category, StrategyPost, Comment

class CategoryAdmin(admin.ModelAdmin):


    list_display = ('id', 'title')

    list_display_links = ('id', 'title')

class StrategyPostAdmin(admin.ModelAdmin):


    list_display = ('id', 'title')

    list_display_links = ('id', 'title')

class CommentAdmin(admin.ModelAdmin):

    list_display = ('target', 'name')

    list_display_links = ('target', 'name')

admin.site.register(Category, CategoryAdmin)

admin.site.register(StrategyPost, StrategyPostAdmin)

admin.site.register(Comment, CommentAdmin)

