from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from reviews.validators import validate_year, validate_username

ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

MAX_LENGTH = 100


class YamdbUser(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя', max_length=MAX_LENGTH, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=MAX_LENGTH, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты.', max_length=254, unique=True,
    )
    bio = models.TextField('Характеристика', blank=True, null=True)
    role = models.CharField(
        default="user", choices=ROLES,
        max_length=max(map(len, dict(ROLES).values()))
    )
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=200, null=True, blank=True
    )
    username = models.CharField(
        verbose_name='Логин', max_length=MAX_LENGTH, unique=True,
        validators=[UnicodeUsernameValidator(), validate_username]
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:30]


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


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField('Описания для отзыва')
    author = models.ForeignKey(
        YamdbUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Описания для отзыва')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'], name='unique_title_author'
        )]

    def __str__(self) -> str:
        return f'{self.title.name}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Описание комментария')
    author = models.ForeignKey(
        YamdbUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления комментария'
    )
    text = models.TextField('Описание комментария')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата добавления комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def str(self) -> str:
        return self.review.text
