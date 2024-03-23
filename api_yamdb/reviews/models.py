from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import YamdbUser

TEXT_SIZE = 30
MIN_VALUE_VALIDATOR = 1
MAX_VALUE_VALIDATOR = 10


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
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска', validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Краткое описание', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    raiting = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
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


class AbstractBaseReviewComment(models.Model):
    """Базовая абстрактная модель комментариев, отзыв."""
    text = models.TextField('Описания')
    author = models.ForeignKey(YamdbUser, on_delete=models.CASCADE,
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата добавления')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:TEXT_SIZE]


class Review(AbstractBaseReviewComment):
    """Модель отзыва на произведение."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN_VALUE_VALIDATOR),
                    MaxValueValidator(MAX_VALUE_VALIDATOR)]
    )

    class Meta(AbstractBaseReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'], name='unique_title_author'
        )]


class Comment(AbstractBaseReviewComment):
    """Модель комментарии на отзыва."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               verbose_name='Отзыв')

    class Meta(AbstractBaseReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
