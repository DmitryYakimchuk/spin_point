# Generated by Django 4.2.9 on 2024-03-26 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='referee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_referee', to=settings.AUTH_USER_MODEL, verbose_name='Судья'),
        ),
        migrations.AddField(
            model_name='teamgame',
            name='team_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamgame_team_1', to='players.team', verbose_name='Первая команда'),
        ),
        migrations.AddField(
            model_name='teamgame',
            name='team_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamgame_team_2', to='players.team', verbose_name='Вторая команда'),
        ),
        migrations.AddField(
            model_name='singlegame',
            name='player_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singlegame_player_1', to=settings.AUTH_USER_MODEL, verbose_name='Первый игрок'),
        ),
        migrations.AddField(
            model_name='singlegame',
            name='player_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singlegame_player_2', to=settings.AUTH_USER_MODEL, verbose_name='Второй игрок'),
        ),
        migrations.AddField(
            model_name='doublesgame',
            name='pair_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doublesgame_pair_1', to='players.doubles', verbose_name='Первая пара'),
        ),
        migrations.AddField(
            model_name='doublesgame',
            name='pair_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doublesgame_pair_2', to='players.doubles', verbose_name='Вторая пара'),
        ),
    ]
