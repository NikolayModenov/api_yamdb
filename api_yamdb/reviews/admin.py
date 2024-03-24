from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, YamdbUser


@admin.register(YamdbUser)
class YamdbUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'confirmation_code', 'bio', 'role'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )


admin.site.register(YamdbUser)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)
