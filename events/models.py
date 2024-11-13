from django.db import models


class Event(models.Model):
    """For meetings players for game or training"""

    class STATUS(models.TextChoices):
        ACTIVE = 'active', 'активно'
        COMPLETED = 'completed', 'завершено'
        CANCELED = 'canceled', 'отменено'

    class OPEN(models.IntegerChoices):
        YES = 1, 'открытое'
        NO = 0, 'закрытое'

    name = models.CharField(max_length=255, verbose_name='Имя события')
    initiator = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='event_initiator',
                                  verbose_name='Инициатор')
    participants = models.ManyToManyField('players.Player', related_name='event_participants',
                                          verbose_name='Участники встречи')
    allowed_participants = models.ManyToManyField('players.Player', blank=True,
                                                  related_name='event_allowed_participants',
                                                  verbose_name='Имеющие права игроки на участие во встрече')
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE,
                              verbose_name="Статус события")
    is_open = models.SmallIntegerField(default=OPEN.YES, choices=OPEN.choices, verbose_name='Статус')
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата и время начала встречи')
    start_time = models.TimeField(null=True, blank=True, verbose_name='Дата и время начала встречи')
    finish_date = models.DateField(null=True, blank=True, verbose_name='Дата и время завершения встречи')
    finish_time = models.TimeField(null=True, blank=True, verbose_name='Дата и время завершения встречи')
    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, null=True, blank=True, related_name='event_club',
                             verbose_name='Клуб')
    city = models.ForeignKey('additions.City', on_delete=models.CASCADE, related_name='event_city',
                             null=True, blank=True, verbose_name='Город')
    addr = models.CharField(max_length=255, verbose_name='Адрес')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    cover = models.ImageField(upload_to='news_covers', null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'

    def __str__(self):
        return f'Событие {self.name}'


class EventComment(models.Model):
    """The model has info about comments of the meeting"""

    commenter = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='eventcomment_commenter',
                                  verbose_name='Комментатор')
    meeting = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventcomment_meeting',
                                verbose_name='Встреча')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Комментарии к встречам'
        verbose_name = 'Комментарий к встрече'

    def __str__(self):
        return f'Комментарий к встрече #{self.meeting}'


class Invitation(models.Model):
    """Needed to invite one player to another"""

    class STATUS(models.TextChoices):
        ACTIVE = 'active', 'активно'
        ACCEPTED = 'accepted', 'принято'
        REJECTED = 'rejected', 'отказано'
        CANCELED = 'canceled', 'отменено'

    initiator = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='invitation_initiator',
                                  verbose_name='Инициатор')
    invited = models.ForeignKey('players.Player', on_delete=models.CASCADE, verbose_name='Приглашенный')
    invitation = models.BooleanField(default=True, verbose_name='Поле для работы уведомлений приглашений')
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE,
                              verbose_name="Статус приглашения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')

    class Meta:
        verbose_name_plural = 'Приглашения'
        verbose_name = 'Приглашение'

    def __str__(self):
        return f'Приглашение #{self.pk}'
