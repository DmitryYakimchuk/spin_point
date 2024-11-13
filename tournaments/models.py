from django.db import models
from django.utils import timezone


class Tournament(models.Model):
    """The model has info about tournament"""

    name = models.CharField(max_length=255, verbose_name='Название турнира')
    description = models.TextField(verbose_name='Описание турнира', null=True, blank=True)
    prizes = models.TextField(verbose_name='Призы турнира', null=True, blank=True)
    start_date = models.DateField(verbose_name='Дата начала турнира')
    finish_date = models.DateField(null=True, verbose_name='Дата окончания турнира')
    participants = models.ManyToManyField('players.Player', related_name='tournament_participants',
                                          verbose_name='Участники турнира')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Турниры'
        verbose_name = 'Турнир'

    def __str__(self):
        return f'Турнир: {self.name}'


class SingleTournament(models.Model):
    """The model has info about single tournament"""

    single_games = models.ManyToManyField('games.SingleGame', related_name='singletournament_games',
                                          verbose_name='Номера игр')

    class Meta:
        verbose_name_plural = 'Одиночные турниры'
        verbose_name = 'Одиночный турнир'

    def __str__(self):
        return f'Одиночный турнир #{self.pk}'


class DoublesTournament(models.Model):
    """The model has info about doubles tournament"""

    doubles = models.ManyToManyField('games.DoublesGame', related_name='doublestournament_doubles',
                                     verbose_name='Пара')
    doubles_games = models.ManyToManyField('games.SingleGame', related_name='doublestournament_games',
                                           verbose_name='Номера игр')

    class Meta:
        verbose_name_plural = 'Парные турниры'
        verbose_name = 'Парный турнир'

    def __str__(self):
        return f'Парный турнир #{self.pk}'


class TeamTournament(models.Model):
    """The model has info about team tournament"""

    teams = models.ManyToManyField('players.Team', related_name='teamtournament_teams', verbose_name='Команда')
    teams_games = models.ManyToManyField('games.TeamGame', related_name='teamstournament_games',
                                           verbose_name='Номера игр')

    class Meta:
        verbose_name_plural = 'Командные турниры'
        verbose_name = 'Командный турнир'

    def __str__(self):
        return f'Командный турнир #{self.pk}'
