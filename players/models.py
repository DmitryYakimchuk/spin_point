from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils import timezone


class Player(AbstractUser):
    """Model has info about user that is player in the project"""

    class SEX(models.IntegerChoices):
        MALE = 1, 'мужской'
        FEMALE = 0, 'женский'

    class HAND(models.IntegerChoices):
        RIGHT = 1, 'правая'
        LEFT = 0, 'левая'

    class SEARCHABLE(models.IntegerChoices):
        YES = 1, 'правая'
        NO = 0, 'левая'

    class STYLE(models.TextChoices):
        ATTACKING = 'attacking', 'атакующий'
        DEFENSIVE = 'defensive', 'защитный'
        MIXED = 'mixed', 'смешанный'
        MASCULINE = 'masculine', 'мужской'
        FEMININE = 'feminine', 'женский'
        SEXLESS = 'sexless', 'бесполый'
        CLUMSY = 'clumsy', 'корявый'
        UGLY = 'ugly', 'стрёмный'
        NERVOUS = 'nervous', 'нервный'
        CALM = 'calm', 'спокойный'

    class LEVEL(models.TextChoices):
        BEGINNER = 'beginner', 'новичок'
        AMATEUR = 'amateur', 'любитель'
        ADVANCED = 'advanced', 'продвинутый'
        EXPERT = 'expert', 'эксперт'
        LEGEND = 'legend', 'легенда'

    class ROLE(models.TextChoices):
        PLAYER_ROLE = 'player', 'игрок'
        REFEREE_ROLE = 'referee', 'судья'
        PR_ROLE = 'player_and_referee', 'игрок и судья'
        TRAINER = 'trainer', 'тренер'
        OTHER_ROLE = 'other', 'другая роль'

    searchable = models.SmallIntegerField(default=SEARCHABLE.YES, choices=SEARCHABLE.choices,
                                          verbose_name='Доступность для вызова другими игроками')
    middle_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отчество')
    birthday = models.DateField(null=True, blank=True, verbose_name='День рождения')
    sex = models.SmallIntegerField(null=True, blank=True, choices=SEX.choices, verbose_name='Пол')
    about = models.TextField(null=True, blank=True, verbose_name='Обо мне')
    photo = models.ImageField(upload_to='players_photo', null=True, blank=True, verbose_name='Аватар')
    role = models.CharField(max_length=20, choices=ROLE.choices, default=ROLE.PLAYER_ROLE, verbose_name='Роль')
    skill_level = models.CharField(max_length=50, default=LEVEL.AMATEUR, choices=LEVEL.choices,
                                   verbose_name='Уровень игры')
    playstyle = models.CharField(max_length=50, null=True, blank=True, choices=STYLE.choices, verbose_name='Стиль игры')
    hand = models.SmallIntegerField(default=HAND.RIGHT, choices=HAND.choices, verbose_name='Игровая рука')
    phone_number = models.CharField(max_length=30, null=True, blank=True, verbose_name='Номер телефона')
    telegram_nick = models.CharField(max_length=65, null=True, blank=True, verbose_name='Никнейм в телеграмме')
    city = models.ForeignKey('additions.City', on_delete=models.CASCADE, related_name='player_city', null=True,
                             verbose_name='Город')
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='ip-адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Игроки'
        verbose_name = 'Игрок'

    def get_absolute_url(self):
        return reverse('players:player_info', kwargs={'username': self.username})

    def __str__(self):
        return f'{self.username}'


User = get_user_model()


class Rating(models.Model):
    """Model has rating for each player depend on date"""

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='rating_player')
    rating_date = models.DateField(default=timezone.now, verbose_name='Дата')
    rating = models.DecimalField(decimal_places=1, max_digits=5, default=1000.0, validators=[MinValueValidator(0)],
                                 verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        ordering = ['rating_date']
        verbose_name_plural = 'Рейтинги игрока'
        verbose_name = 'Рейтинг игрока'

    def __str__(self):
        return f'Рейтинг {self.player} на {self.rating_date}: {self.rating}.'


class Team(models.Model):
    """Model has info about table-tennis team"""

    name = models.CharField(max_length=100, verbose_name='Имя команды')
    logo = models.ImageField(upload_to='teams_logo', null=True, blank=True, verbose_name='Логотип команды')
    description = models.TextField(null=True, blank=True, verbose_name='Описание команды')
    caption = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='team_caption',
                                verbose_name='Капитан команды')
    members = models.ManyToManyField(Player, related_name='team_members', verbose_name='Участники команды')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Команды'
        verbose_name = 'Команда'

    def __str__(self):
        return f'Команда {self.name}'


class Doubles(models.Model):
    """Model has info about 2 team players which is actually one pair"""

    class TYPE(models.IntegerChoices):
        MM = 1, 'мужская пара'
        FF = 2, 'женская пара'
        MF = 3, 'смешанная пара'

    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='doubles_player_1',
                                 verbose_name='1-ый игрок')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='doubles_player_2',
                                 verbose_name='2-ой игрок')
    pair_type = models.PositiveSmallIntegerField(choices=TYPE.choices, verbose_name='Тип пары')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Пары'
        verbose_name = 'Пара'

    def __str__(self):
        return f'Пара #{self.pk}'


class ChatMessage(models.Model):
    """The model has info about chat message"""

    sender = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='chatmessage_sender',
                               verbose_name='Отправитель сообщения')
    receiver = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='chatmessage_receiver',
                                 verbose_name='Получатель сообщения')
    date_time = models.DateTimeField(default=timezone.now, verbose_name='Дата и время отправки сообщения')
    content = models.CharField(max_length=4096, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Чаты'
        verbose_name = 'Чат'

    def __str__(self):
        return f'Сообщение #{self.pk}'

    def clean(self):
        # Checking if sender is not receiver
        if self.sender == self.receiver:
            raise ValidationError('sender and receiver must be different.')

    def save(self, *args, **kwargs):
        self.clean()  # Call clean() before save()
        super().save(*args, **kwargs)


class SearchPartner(models.Model):
    """Model is for searching partner"""
    class STATUS(models.TextChoices):
        ACTIVE = 'active', 'активно'
        COMPLETED = 'completed', 'завершено'
        CANCELED = 'canceled', 'отменено'

    class GAMETYPE(models.TextChoices):
        SINGLE = 'singles', 'одиночная'
        DOUBLES = 'doubles', 'парная'
        TEAM = 'team', 'командная'

    player = models.ForeignKey('players.Player', on_delete=models.CASCADE, verbose_name="Пользователь")
    search_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата поиска")
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE,
                              verbose_name="Статус поиска")
    game_type = models.CharField(max_length=20, choices=GAMETYPE.choices, verbose_name="Тип игры")
    min_rating = models.IntegerField(null=True, blank=True, verbose_name="Минимальный рейтинг")
    max_rating = models.IntegerField(null=True, blank=True, verbose_name="Максимальный рейтинг")
    min_age= models.IntegerField(null=True, blank=True, verbose_name="Минимальный возраст")
    max_age = models.IntegerField(null=True, blank=True, verbose_name="Максимальный возраст")
    skill_level = models.CharField(max_length=50, null=True, blank=True, choices=Player.LEVEL.choices,
                                   verbose_name='Уровень игры')
    playstyle = models.CharField(max_length=50, null=True, blank=True, choices=Player.STYLE.choices,
                                 verbose_name='Стиль игры')
    hand = models.SmallIntegerField(null=True, blank=True, choices=Player.HAND.choices, verbose_name='Игровая рука')
    city = models.ForeignKey('additions.City', on_delete=models.CASCADE, verbose_name="Город")
    message = models.TextField(blank=True, null=True, verbose_name="Сообщение")

    class Meta:
        verbose_name = "Поиск партнёра"
        verbose_name_plural = "Поиски партнёров"

    def __str__(self):
        return f"{self.player.username} - {self.get_game_type_display()} - {self.status}"
