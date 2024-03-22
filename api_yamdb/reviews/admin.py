from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class GenreTitleTab(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [
        GenreTitleTab,
    ]
    list_display = ('name', 'year', 'description', 'raiting', 'category')
    fieldsets = [(None, {
        'fields': ('name', 'year', 'description', 'category')
    }), ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'score', 'pub_date')


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
