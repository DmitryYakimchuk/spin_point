from django import forms
from .models import News, NewsComment
from clubs.models import Club


class NewsCreationForm(forms.ModelForm):
    name = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'm-1'}))
    is_open = forms.BooleanField(label='Доступно для всех', required=False, initial=True,
                                 widget=forms.CheckboxInput(attrs={'class': 'm-1'}))
    keywords = forms.CharField(label='Ключевые слова', required=False, widget=forms.TextInput(attrs={'class': 'm-1'}))
    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'class': 'm-1'}))
    cover = forms.ImageField(label='Обложка', required=False, widget=forms.FileInput(attrs={'class': 'm-1'}))
    club = forms.ModelChoiceField(queryset=None, label='Клуб', required=False,
                                  widget=forms.Select(attrs={'class': 'm-1'}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(NewsCreationForm, self).__init__(*args, **kwargs)

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
        model = News
        fields = ['name', 'club', 'is_open', 'keywords', 'content', 'cover']


class NewsCommentCreationForm(forms.ModelForm):
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class': 'm-1 form-control'}),
                              max_length=5000, min_length=2)

    class Meta:
        model = NewsComment
        fields = ('comment', )