from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')


admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
