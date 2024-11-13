from django.db import models
from django.utils import timezone


class Club(models.Model):
    """The model has info about each club"""

    class OPEN(models.IntegerChoices):
        YES = 1, 'открытый'
        NO = 0, 'закрытый'

    name = models.CharField(max_length=255, verbose_name='Имя клуба', unique=True)
    owner = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='club_owner',
                              verbose_name='Владелец клуба', null=True, blank=True)
    is_open = models.SmallIntegerField(default=OPEN.YES, choices=OPEN.choices, verbose_name='Статус')
    city = models.ForeignKey('additions.City', on_delete=models.CASCADE, related_name='club_city', verbose_name='Город')
    addr = models.CharField(max_length=255, verbose_name='Адрес')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    website = models.CharField(max_length=2500, null=True, blank=True, verbose_name='Сайт')
    logo = models.ImageField(upload_to='clubs_logo', null=True, blank=True, verbose_name='Логотип')
    telegram = models.CharField(max_length=255, null=True, blank=True, verbose_name='Телеграмм')
    members = models.ManyToManyField('players.Player', related_name='club_members', verbose_name='Участники клуба')
    potential_members = models.ManyToManyField('players.Player', blank=True, related_name='potential_club_members',
                                               verbose_name='Потенциальные участники клуба')
    games = models.ManyToManyField('games.Game', blank=True, related_name='club_game', verbose_name='Игры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Клубы'
        verbose_name = 'Клуб'

    def __str__(self):
        return f'{self.name}'


class ClubReview(models.Model):
    """The model exists for reviews about the club"""

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='clubreview_club',
                             verbose_name='Заголовок отзыва')
    text = models.TextField(verbose_name='Текст отзыва')
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='clubreview_player')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def __str__(self):
        return f'Отзыв о клубе {self.club} от пользователя {self.player}'