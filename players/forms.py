from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from .models import Player
from additions.models import City
from clubs.models import Club


class PlayerAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'm-1', 'placeholder': 'your nickname'}),
        label='Username',
        max_length=150,
        min_length=2,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message='Никнейм может состоять только из латинских букв, цифр и знака подчеркивания.'
                        ' Минимум 2 символа.',
                code='invalid_username'
            ),
        ],
        help_text='Имя пользователя может состоять только из латинских букв, цифр и знака подчеркивания.'
                  ' Минимум 2 символа.',
    )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'm-1', 'placeholder': 'Введите пароль'}),
        required=True,
        help_text='Введите корректный пароль.')

    class Meta:
        model = Player
        fields = ('username', 'password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not Player.objects.filter(username__iexact=username).exists():
            raise ValidationError(self.error_messages['invalid_login'])
        return username


class PlayerCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'm-1', 'placeholder': 'Введите Ваше имя'}),
        label='Firstname',
        max_length=150,
        min_length=2,
        validators=[
            RegexValidator(
                regex='^[a-zA-Zа-яА-Я]+$',
                message='Имя может состоять только из букв. Минимум 2 символа.',
                code='invalid_username'
            ),
        ],
        help_text='Имя пользователя может состоять только из букв. Минимум 2 символа.',
    )

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'm-1', 'placeholder': 'Введите Вашу фамилию'}),
        label='Lastname',
        max_length=150,
        min_length=2,
        validators=[
            RegexValidator(
                regex='^[a-zA-Zа-яА-Я]+$',
                message='Фамилия может состоять только из букв. Минимум 2 символа.',
                code='invalid_username'
            ),
        ],
        help_text='Фамилия пользователя может состоять только из букв. Минимум 2 символа.',
    )

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'm-1', 'placeholder': 'your nickname'}),
        label='Username',
        max_length=150,
        min_length=2,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message='Никнейм может состоять только из латинских букв, цифр и знака подчеркивания.'
                        ' Минимум 2 символа.',
                code='invalid_username'
            ),
        ],
        help_text='Имя пользователя может состоять только из латинских букв, цифр и знака подчеркивания.'
                  ' Минимум 2 символа.',
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'm-1', 'placeholder': 'your_email@email.com'}),
                             required=True,
                             help_text='Введите корректный email.')

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'm-1', 'placeholder': 'Введите пароль'}),
        required=True,
        help_text='Введите корректный пароль. Он не должен быть лёгким.')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'm-1', 'placeholder': 'Подтвердите пароль'}),
        required=True,
        help_text='Введите корректный пароль. Он не должен быть лёгким.')

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class PlayerFilterForm(forms.Form):
    username = forms.CharField(label='Имя игрока', required=False, widget=forms.TextInput(
        attrs={'class': 'm-1', 'placeholder': 'никнейм'}),
                               max_length=150,
                               min_length=2,
                               validators=[
                                   RegexValidator(
                                       regex='^[a-zA-Z0-9_]+$',
                                       message='Никнейм может состоять только из латинских букв, цифр и знака подчеркивания.'
                                               ' Минимум 2 символа.',
                                       code='invalid_username'
                                   ),
                               ],
                               help_text='Имя пользователя может состоять только из латинских букв, цифр и знака подчеркивания.'
                                         ' Минимум 2 символа.'
                               )
    sex = forms.ChoiceField(label='Пол', choices=[('', 'Любой')] + list(Player.SEX.choices), required=False,
                            widget=forms.Select(attrs={'class': 'm-1'}))
    min_age = forms.IntegerField(
        label='Минимальный возраст',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'm-1', 'style': 'width: 65px;'}),
        validators=[MinValueValidator(0, message='Возраст не может быть меньше 0'),
                    MaxValueValidator(120, message='Возраст не может быть больше 120')]
    )
    max_age = forms.IntegerField(
        label='Максимальный возраст',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'm-1', 'style': 'width: 65px;'}),
        validators=[MinValueValidator(0, message='Возраст не может быть меньше 0'),
                    MaxValueValidator(120, message='Возраст не может быть больше 120')]
    )
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(), required=False,
                                  empty_label='Укажите город', widget=forms.Select(attrs={'class': 'm-1'}))
    club = forms.ModelChoiceField(label='Клуб', queryset=Club.objects.all(), required=False,
                                  empty_label='Укажите клуб', widget=forms.Select(attrs={'class': 'm-1'}))
    min_rating = forms.DecimalField(
        label='Минимальный рейтинг',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'm-1', 'style': 'width: 65px; display: flex; align-items: center;'}),
        validators=[MinValueValidator(0, message='Рейтинг не может быть меньше 0')]
    )
    max_rating = forms.DecimalField(
        label='Максимальный рейтинг',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'm-1', 'style': 'width: 65px; display: flex; align-items: center;'}),
        validators=[MinValueValidator(0, message='Рейтинг не может быть меньше 0')]
    )
    role = forms.ChoiceField(label='Роль', choices=[('', 'Любая')] + list(Player.ROLE.choices), required=False,
                             widget=forms.Select(attrs={'class': 'm-1'}))
    skill_level = forms.ChoiceField(label='Уровень игры', choices=[('', 'Любой')] + list(Player.LEVEL.choices),
                                    required=False, widget=forms.Select(attrs={'class': 'm-1'}))
    playstyle = forms.ChoiceField(label='Стиль игры', choices=[('', 'Любой')] + list(Player.STYLE.choices),
                                  required=False, widget=forms.Select(attrs={'class': 'm-1'}))
    hand = forms.ChoiceField(label='Игровая рука', choices=[('', 'Любая')] + list(Player.HAND.choices), required=False,
                             widget=forms.Select(attrs={'class': 'm-1'}))
    has_photo = forms.BooleanField(label='С фото', required=False, initial=False,
                                   widget=forms.CheckboxInput(attrs={'class': 'm-1'}))


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'm-1'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'm-1'}))
    middle_name = forms.CharField(label='Отчество', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    phone_number = forms.CharField(label='Телефон', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    telegram_nick = forms.CharField(label='Telegram', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={'class': 'm-1'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(), required=False,
                                  widget=forms.Select(attrs={'class': 'm-1'}))
    sex = forms.ChoiceField(label='Пол', choices=Player.SEX.choices, required=False,
                            widget=forms.Select(attrs={'class': 'm-1'}))
    about = forms.CharField(label='Обо мне', required=False, widget=forms.Textarea(attrs={'class': 'm-1'}))
    role = forms.ChoiceField(label='Роль', choices=[('', '---------')] + list(Player.ROLE.choices), required=False,
                             widget=forms.Select(attrs={'class': 'm-1'}))
    skill_level = forms.ChoiceField(label='Уровень игры', choices=[('', '---------')] + list(Player.LEVEL.choices),
                                    required=False, widget=forms.Select(attrs={'class': 'm-1'}))
    playstyle = forms.ChoiceField(label='Стиль игры', choices=[('', '---------')] + list(Player.STYLE.choices),
                                  required=False, widget=forms.Select(attrs={'class': 'm-1'}))
    hand = forms.ChoiceField(label='Игровая рука', choices=Player.HAND.choices, required=False,
                             widget=forms.Select(attrs={'class': 'm-1'}))

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'middle_name', 'photo', 'about', 'sex', 'role', 'skill_level',
                  'playstyle', 'hand', 'phone_number', 'telegram_nick', 'city')
