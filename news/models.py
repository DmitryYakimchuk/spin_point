from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class News(models.Model):
    """The model has info about news"""

    class OPEN(models.IntegerChoices):
        YES = 1, 'открытая'
        NO = 0, 'закрытая'

    class PUBLISHED(models.IntegerChoices):
        YES = 1, 'опубликовано'
        NO = 0, 'на рассмотрении'

    class DECISION(models.IntegerChoices):
        PUBLISH = 1, 'публиковать'
        REJECT = 0, 'отклонить'

    name = models.CharField(max_length=255, verbose_name='Имя новости')
    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, related_name='news_club',
                             verbose_name='Клуб', null=True, blank=True)
    is_open = models.SmallIntegerField(default=OPEN.YES, choices=OPEN.choices, verbose_name='доступность новости')
    date_time = models.DateTimeField(default=timezone.now, verbose_name='Дата и время новости')
    keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ключевые слова')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='news_author',
                               verbose_name='Автор')
    cover = models.ImageField(upload_to='news_covers', null=True, blank=True, verbose_name='Изображение')
    views_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Просмотры')
    likes_count = models.IntegerField(default=0, verbose_name='Лайки')
    is_published = models.SmallIntegerField(default=PUBLISHED.NO, choices=PUBLISHED.choices, verbose_name='Опубликовано')
    publishing_decision = models.SmallIntegerField(null=True, blank=True, choices=DECISION.choices,
                                                   verbose_name='Решение о публикации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'

    def __str__(self):
        return f'{self.name}'


class NewsComment(models.Model):
    """The model has info about comments of the news"""

    commenter = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='newscomment_commenter',
                                  verbose_name='Комментатор')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='newscomment_news', verbose_name='Новость')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Комментарии к новостям'
        verbose_name = 'Комментарий к новости'

    def __str__(self):
        return f'Комментарий к новости #{self.news}'


class NewsLike(models.Model):
    """The model has info about likes of the news.
    For the news user can like once only."""

    liker = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='newslike_liker',
                              verbose_name='Лайкер')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='newslike_news', verbose_name='Новость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Лайки к новости'
        verbose_name = 'Лайк к новости'
        unique_together = (('liker', 'news'),)

    def __str__(self):
        return f'Лайк пользователя {self.liker.username} на новость "{self.news}"'
