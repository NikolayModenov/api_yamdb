from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models


ROLES = ("user", "moderator", "admin",)


class MyUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(default="user", choices=ROLES)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(max_length=4)
    # description = models.CharField()
    # genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.OneToOneField(
        Category, on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'произведения'
        verbose_name_plural = 'Произведение'
        default_related_name = 'titles'

    def __str__(self) -> str:
        return f'{self.pk}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        #   related_name='posts'
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
        User, on_delete=models.CASCADE,
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
