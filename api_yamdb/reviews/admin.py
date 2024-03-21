from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text')


admin.site.register(Category)
admin.site.register(Genre)
