import os
import random
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.generic import ListView, View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Invitation, Event
from .forms import PlayerCreationForm, PlayerAuthenticationForm, PlayerFilterForm, UserProfileForm
from .models import Player, Rating
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from notifications.signals import notify
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from clubs.models import Club
from news.models import News
# from .serializers import PlayersSerializer
from .serializers import RatingSerializer, PlayersRatingSerializer
from utils.players_filters import get_filtered_players, get_player_last_rating_position
from utils.general import logout_required


def get_players_index_page(request: HttpRequest) -> HttpResponse:
    """
    The view returns ratings and corresponding positions for players.
    There is the filters options as well for:
    - username
    - rating
    - age
    - sex
    - city
    - role
    - skill level
    - playstyle
    - playing hand
    - is_photo - in process
    """

    form, players = get_filtered_players(request)

    # Show 15 players per page
    page = int(request.GET.get("page", 1))
    per_page = 10
    start = (page - 1) * per_page

    paginator = Paginator(players, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'rating_page': True,
        'start': start,
    }
    return render(request, 'players/index.html', context)


def get_player_info(request: HttpRequest, username: str) -> HttpResponse:
    """The view is for getting info about the user"""

    player = get_object_or_404(Player, username=username)

    context = {
        'player': player,
        'player_last_rating': Rating.objects.filter(player=player).last().rating,
        'player_last_position': get_player_last_rating_position(username),
    }
    return render(request, 'players/player_info.html', context)


# def change_rating(request: HttpRequest) -> HttpResponse:
#     numbers = list(range(101))
#     days = list(range(1, 31))
#     players = Player.objects.all()
#     coin = [1, 0]
#     for player in players:
#         last_rating = Rating.objects.all().last().rating
#         for day in days[:random.choice(days)]:
#             if random.choice(coin):
#                 Rating.objects.create(player=player, rating=(last_rating + random.choice(numbers)),
#                                       rating_date=date(2024, 3, day))
#             else:
#                 Rating.objects.create(player=player, rating=(last_rating - random.choice(numbers)),
#                                       rating_date=date(2024, 3, day))
#     return HttpResponse('Rating was added successfully!')


class AllNotificationListView(ListView):
    model = Notification
    template_name = 'players/notifications.html'
    context_object_name = 'custom_notifications'
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.notifications.filter(deleted=False).prefetch_related('actor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club_content_type = ContentType.objects.get_for_model(Club)
        news_content_type = ContentType.objects.get_for_model(News)
        player_content_type = ContentType.objects.get_for_model(Player)
        invitation_content_type = ContentType.objects.get_for_model(Invitation)
        event_content_type = ContentType.objects.get_for_model(Event)

        context['club_notification_count'] = self.request.user.notifications. \
            filter(target_content_type=club_content_type, unread=True).count()
        context['news_notification_count'] = self.request.user.notifications. \
            filter(target_content_type=news_content_type, unread=True).count()
        context['player_notification_count'] = self.request.user.notifications. \
            filter(target_content_type=player_content_type, unread=True).count()
        context['invitation_content_count'] = self.request.user.notifications. \
            filter(target_content_type=invitation_content_type, unread=True).count()
        context['event_content_count'] = self.request.user.notifications. \
            filter(target_content_type=event_content_type, unread=True).count()

        context['title'] = f'Все уведомления'
        return context


class InvitationNotificationListView(AllNotificationListView):
    def get_queryset(self):
        club_content_type = ContentType.objects.get_for_model(Invitation)
        return self.request.user.notifications.filter(target_content_type=club_content_type, deleted=False). \
            prefetch_related('actor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Мои приглашения'
        return context


class EventNotificationListView(AllNotificationListView):
    def get_queryset(self):
        event_content_type = ContentType.objects.get_for_model(Event)
        return self.request.user.notifications.filter(target_content_type=event_content_type, deleted=False). \
            prefetch_related('actor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Мои события'
        return context


class ClubNotificationListView(AllNotificationListView):
    def get_queryset(self):
        club_content_type = ContentType.objects.get_for_model(Club)
        return self.request.user.notifications.filter(target_content_type=club_content_type, deleted=False). \
            prefetch_related('actor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Уведомления от клубов'
        return context


class NewsNotificationListView(AllNotificationListView):
    def get_queryset(self):
        news_content_type = ContentType.objects.get_for_model(News)
        return self.request.user.notifications.filter(target_content_type=news_content_type, deleted=False). \
            prefetch_related('actor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Новостные уведомления'
        return context


class NotificationActions(View):
    def post(self, request):
        action = request.POST.get('action')
        notification_pk = request.POST.get('notification_pk')

        try:
            notification = self.request.user.notifications.get(pk=notification_pk)
            if action == 'mark_as_read':
                notification.unread = False
                notification.save()
                return JsonResponse({'success': True})
            elif action == 'delete':
                notification.unread = False
                notification.deleted = True
                notification.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})


@logout_required
def register_view(request):
    if request.method == 'POST':
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Действия при успешной регистрации

            # Adding default rating to the player
            player = form.cleaned_data.get('username')
            new_player = Player.objects.get(username=player)
            Rating.objects.create(player=new_player)

            return redirect('players:login')
    else:
        form = PlayerCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@logout_required
def login_view(request: HttpRequest) -> HttpResponse:
    login_error = "Пожалуйста, введите правильные логин и пароль. " \
                  "Оба поля могут быть чувствительны к регистру."
    if request.method == 'POST':
        form = PlayerAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            player = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=player, password=password)
            if user is not None:
                login(request, user)
                return redirect('players:profile')
    else:
        form = PlayerAuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form, 'login_error': login_error})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logout(request)
    return redirect('players:index')


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Personal user info with rating"""

    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('players:profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Личный кабинет',
        'form': form,
        'player_last_rating': Rating.objects.filter(player=request.user).last().rating,
        'player_last_position': get_player_last_rating_position(request.user.username),
    }
    return render(request, 'players/profile.html', context)


def get_rating_data(player: Player) -> list:
    ratings = Rating.objects.filter(player=player).order_by('created_at')
    return [[rating.rating_date, rating.rating] for rating in ratings]


def plot_rating_graph(request: HttpRequest, username: str) -> JsonResponse:
    player = get_object_or_404(Player, username=username)
    data = get_rating_data(player)
    return JsonResponse({'data': data})


class PlayersRatingAPIView(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersRatingSerializer


def validate_username(request: HttpRequest) -> JsonResponse:
    """Checking if the username has already existed by AJAX"""

    response_data = {}
    if request.GET:
        username = request.GET.get('username')
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return JsonResponse({
                'username_invalid': 'Никнейм может состоять только из латинских символов, цифр, дефиса и знака подчеркивания.'})
        username_taken = Player.objects.filter(username=username).exists()
        if username_taken:
            response_data['username_taken'] = 'Этот никнейм уже занят'
    return JsonResponse(response_data)


def validate_email(request) -> JsonResponse:
    """Checking if the email has already existed by AJAX"""

    response_data = {}
    if request.GET:
        email = request.GET.get('email')
        email_taken = Player.objects.filter(email=email).exists()
        if email_taken:
            response_data['email_taken'] = 'Этот почтовый адрес уже занят'
    return JsonResponse(response_data)


def validate_password_view(request: HttpRequest) -> JsonResponse:
    """Checking if the password valid in registration form by AJAX"""

    if request.GET:
        password = request.GET.get('password')

        # Checking minimum  length
        if len(password) < 8:
            return JsonResponse({'password_invalid': 'Пароль должен содержать минимум 8 символов.'})

        # Checking if the password contains at least one upper, one lower and one digital symbol
        if not any(char.isupper() for char in password):
            return JsonResponse({'password_invalid': 'Пароль должен содержать хотя бы одну заглавную букву.'})
        if not any(char.islower() for char in password):
            return JsonResponse({'password_invalid': 'Пароль должен содержать хотя бы одну строчную букву.'})
        if not any(char.isdigit() for char in password):
            return JsonResponse({'password_invalid': 'Пароль должен содержать хотя бы одну цифру.'})

        # Other Django validation, for instance "password is too easy" and so on
        try:
            validate_password(password)
        except ValidationError as e:
            return JsonResponse({'password_invalid': e.messages[0]})

        return JsonResponse({})

# class PlayersInfoAPIView(APIView):
#     def get(self, request: HttpRequest):
#         lst = Player.objects.all().values()
#         return Response({'usernames': list(lst)})
#
#     def post(self, request: HttpRequest):
#         return Response({'username': 'Dima-Dima'})
