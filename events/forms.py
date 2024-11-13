from django import forms
from django.core.validators import MinValueValidator
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware

from clubs.models import Club
from .models import Event
from additions.models import City


class EventCreationForm(forms.ModelForm):
    name = forms.CharField(label='Название события', widget=forms.TextInput(attrs={'class': 'm-1'}))
    is_open = forms.ChoiceField(label='Открытый/закрытый', choices=Event.OPEN.choices,
                                widget=forms.Select(attrs={'class': 'm-1'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'm-1'}))
    club = forms.ModelChoiceField(queryset=None, label='Клуб', required=False,
                                  widget=forms.Select(attrs={'class': 'm-1'}))
    start_date = forms.DateField(label='Дата начала встречи', widget=forms.SelectDateWidget(attrs={'class': 'm-1'}))
    start_time = forms.TimeField(label='Время начала встречи', widget=forms.Select(
        choices=[(datetime.strptime(str(i), '%H').time(), datetime.strptime(str(i), '%H').
                  strftime('%H:%M')) for i in range(24)], attrs={'class': 'm-1'}))
    finish_date = forms.DateField(label='Дата завершения встречи', widget=forms.SelectDateWidget(attrs={'class': 'm-1'}))
    finish_time = forms.TimeField(label='Время завершения встречи', widget=forms.Select(
        choices=[(datetime.strptime(str(i), '%H').time(), datetime.strptime(str(i), '%H').
                  strftime('%H:%M')) for i in range(24)], attrs={'class': 'm-1'}))
    addr = forms.CharField(label='Адрес', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={'class': 'm-1'}))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get("start_date")
    #     start_time = cleaned_data.get("start_time")
    #     finish_date = cleaned_data.get("finish_date")
    #     finish_time = cleaned_data.get("finish_time")
    #
    #     if start_date and start_time and finish_date and finish_time:
    #         start_datetime = datetime.combine(start_date, start_time)
    #         finish_datetime = datetime.combine(finish_date, finish_time)
    #
    #         if start_datetime >= finish_datetime:
    #             raise forms.ValidationError("Дата и время завершения должны быть позже даты и времени начала.")
    #
    #         if start_datetime <= make_aware(datetime.now(), timezone.utc):
    #             raise forms.ValidationError("Дата и время начала должны быть позже текущей даты и времени.")
    #
    #     return cleaned_data
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(EventCreationForm, self).__init__(*args, **kwargs)

        if request:
            # Получаем текущего пользователя из запроса
            user = request.user

            # Получаем клубы, в которых пользователь является членом
            clubs = Club.objects.filter(members__in=[user])

            # Отфильтровать клубы, доступные текущему пользователю
            self.fields['club'].queryset = clubs

            # Добавить пустое значение в список клубов
            choices = list(self.fields['club'].choices)
            self.fields['club'].choices = choices

    class Meta:
        model = Event
        fields = ['name', 'is_open', 'start_time', 'start_date', 'finish_time', 'finish_date',
                  'city', 'club', 'addr', 'description']
