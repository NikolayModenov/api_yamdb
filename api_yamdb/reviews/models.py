from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import YamdbUser


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=256, verbose_name='Hазвание жанра')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='slug')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    year = models.IntegerField(
        max_length=4,
        verbose_name='Год выпуска',
        validators=(validate_year,),)
    category = models.OneToOneField(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year',)

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE,
        #   related_name='posts'
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        # verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'произведения'
        verbose_name_plural = 'Произведение'
        default_related_name = 'rewiews'
        # ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE,
        #   related_name='posts'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        # verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'произведения'
        verbose_name_plural = 'Произведение'
        default_related_name = 'comments'
        # ordering = ('-pub_date',)
