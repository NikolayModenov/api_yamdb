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


admin.site.register(YamdbUser)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
