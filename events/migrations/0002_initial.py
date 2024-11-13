# Generated by Django 4.2.9 on 2024-03-26 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('additions', '0001_initial'),
        ('clubs', '0002_initial'),
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_initiator', to=settings.AUTH_USER_MODEL, verbose_name='Инициатор'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='invited',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Приглашенный'),
        ),
        migrations.AddField(
            model_name='eventcomment',
            name='commenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventcomment_commenter', to=settings.AUTH_USER_MODEL, verbose_name='Комментатор'),
        ),
        migrations.AddField(
            model_name='eventcomment',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventcomment_meeting', to='events.event', verbose_name='Встреча'),
        ),
        migrations.AddField(
            model_name='event',
            name='allowed_participants',
            field=models.ManyToManyField(blank=True, related_name='event_allowed_participants', to=settings.AUTH_USER_MODEL, verbose_name='Имеющие права игроки на участие во встрече'),
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_city', to='additions.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='event',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_club', to='clubs.club', verbose_name='Клуб'),
        ),
        migrations.AddField(
            model_name='event',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_initiator', to=settings.AUTH_USER_MODEL, verbose_name='Инициатор'),
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='event_participants', to=settings.AUTH_USER_MODEL, verbose_name='Участники встречи'),
        ),
    ]
