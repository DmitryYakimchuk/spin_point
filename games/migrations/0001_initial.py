# Generated by Django 4.2.9 on 2024-03-26 16:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('additions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_l', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='Левая часть счёта')),
                ('result_r', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='Правая часть счёта')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время игры')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Заметки по игре')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_city', to='additions.city', verbose_name='Город')),
            ],
        ),
        migrations.CreateModel(
            name='DoublesGame',
            fields=[
                ('game_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='games.game')),
            ],
            options={
                'verbose_name': 'Парная игра',
                'verbose_name_plural': 'Парные игры',
            },
            bases=('games.game',),
        ),
        migrations.CreateModel(
            name='SingleGame',
            fields=[
                ('game_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='games.game')),
            ],
            options={
                'verbose_name': 'Одиночная игра',
                'verbose_name_plural': 'Одиночные игры',
            },
            bases=('games.game',),
        ),
        migrations.CreateModel(
            name='TeamGame',
            fields=[
                ('game_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='games.game')),
            ],
            options={
                'verbose_name': 'Командная игра',
                'verbose_name_plural': 'Командные игры',
            },
            bases=('games.game',),
        ),
    ]
