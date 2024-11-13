# Generated by Django 4.2.9 on 2024-03-26 16:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('additions', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('searchable', models.SmallIntegerField(choices=[(1, 'правая'), (0, 'левая')], default=1, verbose_name='Доступность для вызова другими игроками')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('sex', models.SmallIntegerField(blank=True, choices=[(1, 'мужской'), (0, 'женский')], null=True, verbose_name='Пол')),
                ('about', models.TextField(blank=True, null=True, verbose_name='Обо мне')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='players_photo', verbose_name='Аватар')),
                ('role', models.CharField(choices=[('player', 'игрок'), ('referee', 'судья'), ('player_and_referee', 'игрок и судья'), ('trainer', 'тренер'), ('other', 'другая роль')], default='player', max_length=20, verbose_name='Роль')),
                ('skill_level', models.CharField(choices=[('beginner', 'новичок'), ('amateur', 'любитель'), ('advanced', 'продвинутый'), ('expert', 'эксперт'), ('legend', 'легенда')], default='amateur', max_length=50, verbose_name='Уровень игры')),
                ('playstyle', models.CharField(blank=True, choices=[('attacking', 'атакующий'), ('defensive', 'защитный'), ('mixed', 'смешанный'), ('masculine', 'мужской'), ('feminine', 'женский'), ('sexless', 'бесполый'), ('clumsy', 'корявый'), ('ugly', 'стрёмный'), ('nervous', 'нервный'), ('calm', 'спокойный')], max_length=50, null=True, verbose_name='Стиль игры')),
                ('hand', models.SmallIntegerField(choices=[(1, 'правая'), (0, 'левая')], default=1, verbose_name='Игровая рука')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона')),
                ('telegram_nick', models.CharField(blank=True, max_length=65, null=True, verbose_name='Никнейм в телеграмме')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='ip-адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_city', to='additions.city', verbose_name='Город')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Игрок',
                'verbose_name_plural': 'Игроки',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя команды')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='teams_logo', verbose_name='Логотип команды')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание команды')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('caption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_caption', to=settings.AUTH_USER_MODEL, verbose_name='Капитан команды')),
                ('members', models.ManyToManyField(related_name='team_members', to=settings.AUTH_USER_MODEL, verbose_name='Участники команды')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='SearchPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата поиска')),
                ('status', models.CharField(choices=[('active', 'активно'), ('completed', 'завершено'), ('canceled', 'отменено')], default='active', max_length=20, verbose_name='Статус поиска')),
                ('game_type', models.CharField(choices=[('singles', 'одиночная'), ('doubles', 'парная'), ('team', 'командная')], max_length=20, verbose_name='Тип игры')),
                ('min_rating', models.IntegerField(blank=True, null=True, verbose_name='Минимальный рейтинг')),
                ('max_rating', models.IntegerField(blank=True, null=True, verbose_name='Максимальный рейтинг')),
                ('min_age', models.IntegerField(blank=True, null=True, verbose_name='Минимальный возраст')),
                ('max_age', models.IntegerField(blank=True, null=True, verbose_name='Максимальный возраст')),
                ('skill_level', models.CharField(blank=True, choices=[('beginner', 'новичок'), ('amateur', 'любитель'), ('advanced', 'продвинутый'), ('expert', 'эксперт'), ('legend', 'легенда')], max_length=50, null=True, verbose_name='Уровень игры')),
                ('playstyle', models.CharField(blank=True, choices=[('attacking', 'атакующий'), ('defensive', 'защитный'), ('mixed', 'смешанный'), ('masculine', 'мужской'), ('feminine', 'женский'), ('sexless', 'бесполый'), ('clumsy', 'корявый'), ('ugly', 'стрёмный'), ('nervous', 'нервный'), ('calm', 'спокойный')], max_length=50, null=True, verbose_name='Стиль игры')),
                ('hand', models.SmallIntegerField(blank=True, choices=[(1, 'правая'), (0, 'левая')], null=True, verbose_name='Игровая рука')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Сообщение')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='additions.city', verbose_name='Город')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Поиск партнёра',
                'verbose_name_plural': 'Поиски партнёров',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('rating', models.DecimalField(decimal_places=1, default=1000.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Рейтинг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_player', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рейтинг игрока',
                'verbose_name_plural': 'Рейтинги игрока',
                'ordering': ['rating_date'],
            },
        ),
        migrations.CreateModel(
            name='Doubles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair_type', models.PositiveSmallIntegerField(choices=[(1, 'мужская пара'), (2, 'женская пара'), (3, 'смешанная пара')], verbose_name='Тип пары')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('player_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubles_player_1', to=settings.AUTH_USER_MODEL, verbose_name='1-ый игрок')),
                ('player_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubles_player_2', to=settings.AUTH_USER_MODEL, verbose_name='2-ой игрок')),
            ],
            options={
                'verbose_name': 'Пара',
                'verbose_name_plural': 'Пары',
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время отправки сообщения')),
                ('content', models.CharField(max_length=4096, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage_receiver', to=settings.AUTH_USER_MODEL, verbose_name='Получатель сообщения')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage_sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель сообщения')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
            },
        ),
    ]
