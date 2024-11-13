from django import forms
from django.core.validators import MinValueValidator

from .models import Club
from additions.models import City


class ClubCreationForm(forms.ModelForm):
    name = forms.CharField(label='Название клуба', widget=forms.TextInput(attrs={'class': 'm-1'}))
    is_open = forms.ChoiceField(label='Открытый/закрытый', choices=Club.OPEN.choices,
                                widget=forms.Select(attrs={'class': 'm-1'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'm-1'}))
    addr = forms.CharField(label='Адрес', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={'class': 'm-1'}))
    website = forms.CharField(label='Веб-сайт', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    logo = forms.ImageField(label='Логотип', required=False, widget=forms.FileInput(attrs={'class': 'm-1'}))
    telegram = forms.CharField(label='Telegram', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))

    class Meta:
        model = Club
        fields = ['name', 'is_open', 'city', 'addr', 'description',
                  'website', 'logo', 'telegram']


class ClubsFilterForm(forms.Form):
    name = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    is_open = forms.ChoiceField(label='Статус', required=False, choices=[('', 'Любой')] + list(Club.OPEN.choices),
                                widget=forms.Select(attrs={'class': 'm-1'}))
    city = forms.ModelChoiceField(label='Город', required=False, queryset=City.objects.all(),
                                  empty_label='Укажите город', widget=forms.Select(attrs={'class': 'm-1'}))
    min_participants = forms.IntegerField(
        label='Минимум участников',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'm-1', 'style': 'width: 65px; display: flex; align-items: center;'}),
        validators=[MinValueValidator(1, message='Участников клуба не может быть менее одного.')]
    )
    max_participants = forms.IntegerField(
        label='Максимум участников',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'm-1', 'style': 'width: 65px; display: flex; align-items: center;'}),
        validators=[MinValueValidator(1, message='Участников клуба не может быть менее одного.')]
    )
    has_logo = forms.BooleanField(label='С логотипом', required=False, initial=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'm-1'}))


    class Meta:
        model = Club
        fields = ['name', 'min_participants', 'max_participants', 'city', 'is_open', 'has_logo']
