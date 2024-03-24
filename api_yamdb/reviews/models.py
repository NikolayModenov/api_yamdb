from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from reviews.validators import validate_year, validate_username


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)

MAX_LENGTH = 100
TEXT_SIZE = 30
MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10


class YamdbUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты.', max_length=254, unique=True,
    )
    bio = models.TextField('Характеристика', blank=True, null=True)
    role = models.CharField(
        'Должность', default=USER, choices=ROLES,
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

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff


class CategoryGenreBase(models.Model):
    """Базовая модель для моделей категории и жанра"""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        db_index=True,
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Идентификатор',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Category(CategoryGenreBase):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска', validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Краткое описание', blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:30]


class ReviewCommentBase(models.Model):
    """Базовая абстрактная модель комментариев, отзыв."""
    text = models.TextField('Описание')
    author = models.ForeignKey(YamdbUser, on_delete=models.CASCADE,
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата добавления')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:TEXT_SIZE]


class Review(ReviewCommentBase):
    """Модель отзыва на произведение."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN_SCORE_VALUE),
                    MaxValueValidator(MAX_SCORE_VALUE)]
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'], name='unique_title_author'
        )]


class Comment(ReviewCommentBase):
    """Модель комментарии на отзыва."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               verbose_name='Отзыв')

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
