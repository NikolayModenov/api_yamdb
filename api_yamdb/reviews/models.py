from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models


ROLES = ("user", "moderator", "admin",)


# class MyUser(AbstractUser):
#     bio = models.TextField('Биография', blank=True)
#     role = models.CharField(default="user", choices=ROLES)
from reviews.validators import validate_year
from users.models import YamdbUser


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    # def __str__(self) -> str:
    #     return self.name
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

    # def __str__(self) -> str:
    #     return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    # year = models.IntegerField(max_length=4)
    # description = models.CharField()
    # genre = models.ManyToManyField(Genre, through='GenreTitle')
    year = models.PositiveSmallIntegerField(
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

    # def __str__(self) -> str:
    #     return f'{self.pk}'
    #     ordering = ('-year',)

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    # title_id = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='comments'
    # )
    text = models.TextField()
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE,)
    #     #   related_name='posts'
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
    )
    # text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE,
        related_name='reviews'
    )
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
        # constraints = [
        #     models.UniqueConstraint(fields=['title', 'author'],
        #                             name='unique_title_author')
        # ]

    def __str__(self) -> str:
        return f'{self.pk}'


class Comment(models.Model):
    review_id = models.ForeignKey(
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self) -> str:
        return self.review.text
