from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Game(models.Model):
    """The model has info about the game"""

    SETS = [(i, str(i)) for i in range(11)]  # limits for game sets is 20. It is completely enough
    # The result of the game can be 2:0, 2:3, 4:2 etc. So we have divided result: right and left
    # This way allows to calculate statistics easier than if we could have just string result '2:0', '4:1'...
    result_l = models.IntegerField(choices=SETS, verbose_name='Левая часть счёта')
    result_r = models.IntegerField(choices=SETS, verbose_name='Правая часть счёта')
    referee = models.ForeignKey('players.Player', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Судья', related_name='game_referee')
    date_time = models.DateTimeField(default=timezone.now, verbose_name='Дата и время игры')
    notes = models.TextField(null=True, blank=True, verbose_name='Заметки по игре')
    city = models.ForeignKey('additions.City', on_delete=models.CASCADE, related_name='game_city', null=True,
                             verbose_name='Город')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')


class SingleGame(Game):
    """The model has info about single type of game"""

    player_1 = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='singlegame_player_1',
                                 verbose_name='Первый игрок')
    player_2 = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='singlegame_player_2',
                                 verbose_name='Второй игрок')

    def clean(self):
        # Checking if player_1 is not player_2
        if self.player_1 == self.player_2:
            raise ValidationError('player_1 and player_2 must be different.')

    def save(self, *args, **kwargs):
        self.clean()  # Call clean() before save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Одиночные игры'
        verbose_name = 'Одиночная игра'

    def __str__(self):
        return f'Одиночная игра между {self.player_1} и {self.player_2} #pk={self.pk}'


class DoublesGame(Game):
    """The model has info about doubles type of game"""

    pair_1 = models.ForeignKey('players.Doubles', on_delete=models.CASCADE, related_name='doublesgame_pair_1',
                               verbose_name='Первая пара')
    pair_2 = models.ForeignKey('players.Doubles', on_delete=models.CASCADE, related_name='doublesgame_pair_2',
                               verbose_name='Вторая пара')

    def clean(self):
        # Checking if pair_1 is not pair_2
        if self.pair_1 == self.pair_2:
            raise ValidationError('pair_1 and pair_2 must be different.')

    def save(self, *args, **kwargs):
        self.clean()  # Call clean() before save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Парные игры'
        verbose_name = 'Парная игра'

    def __str__(self):
        return f'Парная игра между {self.pair_1} и {self.pair_2} #pk={self.pk}'


class TeamGame(Game):
    """The model has info about team type of game"""

    team_1 = models.ForeignKey('players.Team', on_delete=models.CASCADE, related_name='teamgame_team_1',
                               verbose_name='Первая команда')
    team_2 = models.ForeignKey('players.Team', on_delete=models.CASCADE, related_name='teamgame_team_2',
                               verbose_name='Вторая команда')

    def clean(self):
        # Checking if team_1 is not team_2
        if self.team_1 == self.team_2:
            raise ValidationError('team_1 and team_2 must be different.')

    def save(self, *args, **kwargs):
        self.clean()  # Call clean() before save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Командные игры'
        verbose_name = 'Командная игра'

    def __str__(self):
        return f'Командная игра между {self.team_1} и {self.team_2} #pk={self.pk}'
