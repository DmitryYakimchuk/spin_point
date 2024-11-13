from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Exists, OuterRef
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms import ClubCreationForm, ClubsFilterForm
from players.models import Player
from utils.players_filters import get_ordered_rating_and_position_players_queryset
from .models import Club, ClubReview
from news.views import PublicNewsDetailView
from news.models import News, NewsLike

import random
from notifications.signals import notify


class ClubView(DetailView):
    model = Club
    template_name = 'clubs/club.html'
    context_object_name = 'club'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club_page'] = True
        context['title'] = context['club'].name
        return context


class ClubPlayersList(ListView):
    model = Player
    template_name = 'clubs/club_participants.html'
    context_object_name = 'players'
    paginate_by = 10

    def get_queryset(self):
        club_pk = self.kwargs.get('pk')
        players = Club.objects.get(pk=club_pk).members.all()
        return get_ordered_rating_and_position_players_queryset(players)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        club_pk = self.kwargs.get('pk')
        context['club'] = Club.objects.get(pk=club_pk)

        page = int(self.request.GET.get("page", 1))
        start = (page - 1) * self.paginate_by
        context['start'] = start

        return context


class ClubList(ListView):
    """View all the club.There is the filtration options as well"""

    model = Club
    template_name = 'clubs/clubs_list.html'
    context_object_name = 'clubs'
    paginate_by = 2
    form_class = ClubsFilterForm
    extra_context = {
        'title': 'Клубы',
    }

    def get_queryset(self):
        clubs = Club.objects.all().select_related('city', 'owner').prefetch_related('members')
        form = ClubsFilterForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name').strip()
            is_open = form.cleaned_data.get('is_open')
            city = form.cleaned_data.get('city')
            has_logo = form.cleaned_data.get('has_logo')
            min_participants = form.cleaned_data.get('min_participants')
            max_participants = form.cleaned_data.get('max_participants')

            if name:
                clubs = clubs.filter(name__icontains=name)
            if is_open:
                clubs = clubs.filter(is_open=is_open)
            if city:
                clubs = clubs.filter(city=city)
            if has_logo:
                clubs = clubs.exclude(logo='')
            if min_participants:
                clubs = clubs.annotate(num_members=Count('members')).filter(num_members__gte=min_participants)
            if max_participants:
                clubs = clubs.annotate(num_members=Count('members')).filter(num_members__lte=max_participants)

        return clubs.order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class(self.request.GET)
        context['clubs_count'] = self.get_queryset().annotate(Count('pk')).count()
        return context


class MyClubList(LoginRequiredMixin, ClubList):
    """If the user is authenticated he/she will get a club list where the user is owner"""

    login_url = reverse_lazy('players:login')
    extra_context = {
        'title': 'Мои клубы',
        'players_clubs': True,
    }

    def get_queryset(self):
        """Get only the clubs where the user is owner"""
        return super().get_queryset().filter(owner=self.request.user)


class ParticipationClubList(LoginRequiredMixin, ClubList):
    """If the user is authenticated he/she will get a club list where the user is a member"""

    login_url = reverse_lazy('players:login')
    extra_context = {
        'title': 'Клубы с моим участие',
        'player_participant_in_club': True,
    }

    def get_queryset(self):
        """Get only the clubs where the user is in the members list"""
        return super().get_queryset().filter(members__in=[self.request.user])


class ClubCreationView(LoginRequiredMixin, CreateView):
    """Creating the club and automatically adding user to owner and members fields"""

    model = Club
    form_class = ClubCreationForm
    template_name = 'clubs/create_club.html'
    login_url = reverse_lazy('players:login')
    success_url = reverse_lazy('clubs:my_clubs')
    extra_context = {
        'title': 'Создание нового клуба',
    }

    def form_valid(self, form):
        """Because of members is ManyToMany field
         we cannot save object with value player to members simultaneously.
         At the first step we create and save Club object with empty members filed.
         And then we can add the player (owner) to members list"""

        club = form.save(commit=False)
        player = Player.objects.get(username=self.request.user.username)
        club.owner = player
        club.save()
        club.members.add(player)
        return super().form_valid(form)


class UpdateClubView(LoginRequiredMixin, UpdateView):
    """For changing club information/data.
    Only owner can modify data of the club"""

    model = Club
    fields = ['name', 'is_open', 'city', 'addr', 'description', 'website', 'telegram', 'logo']
    template_name = 'clubs/edit_club.html'
    login_url = reverse_lazy('players:login')
    success_url = reverse_lazy('clubs:my_clubs')
    extra_context = {
        'title': 'Редактирование клуба',
    }

    def get_queryset(self):
        """Making SQL query better"""
        return super().get_queryset().select_related('owner')

    def dispatch(self, request, *args, **kwargs):
        """Checking if the user is owner of the club.
        If it is not redirect will happen. If it is everything will ok"""

        self.club = self.get_object()
        if self.club.owner != request.user:
            return redirect('clubs:my_clubs')

        return super().dispatch(request, *args, **kwargs)


def get_random_review_for_club(club: Club) -> tuple[Player, str]:
    """Function returns author object and his/her review for the club """

    club_review_pks = ClubReview.objects.filter(club=club).values_list('pk', flat=True)
    random_club_review = ClubReview.objects.get(pk=random.choice(club_review_pks))
    return random_club_review.player, random_club_review.text


class ClubNewsListView(ListView):
    model = News
    template_name = 'clubs/club_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        """Mark news if the user is already liked the news"""
        news = News.objects.filter(club=self.kwargs.get('club_pk'), is_published=News.PUBLISHED.YES). \
            select_related('club', 'author')
        user_id = self.request.user.pk
        news = news.annotate(liker=Exists(NewsLike.objects.filter(news_id=OuterRef('pk'), liker_id=user_id)))
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs.get('club_pk'))
        context['title'] = f'Новости клуба {club.name}'
        context['club'] = club
        return context


class ClubNewsDetailView(PublicNewsDetailView):
    template_name = 'clubs/club_news_detail.html'

    def get_queryset(self):
        club_pk = self.kwargs.get('club_pk')
        news_pk = self.kwargs.get('pk')
        return News.objects.select_related('club', 'author'). \
            filter(pk=news_pk, club_id=club_pk, is_published=News.PUBLISHED.YES)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(pk=self.kwargs.get('club_pk'))
        return context


def add_to_open_club_members(request: HttpRequest, club_pk: int) -> HttpResponse:
    club = get_object_or_404(Club, pk=club_pk)
    if club.is_open and request.user not in club.members.all():
        club.members.add(request.user)
    return redirect('clubs:club', pk=club_pk)


def add_player_to_potential_club_members(request: HttpRequest, club_pk: int) -> JsonResponse:
    response_data = {}
    club = get_object_or_404(Club, pk=club_pk)
    if not club.is_open:
        if (request.user not in club.members.all()) and (request.user not in club.potential_members.all()):
            club.potential_members.add(request.user)
            message = f"Пользователь {request.user} подал заявку на вступление в клуб ---{club.name}---"
            notify.send(sender=request.user, recipient=club.owner, verb=message, target=club)
            response_data['success'] = True
            return JsonResponse(response_data)
        raise Http404("You have already been in members list of the club.")
    raise Http404("Club is open. You don't have to try to apply to it. You can join it directly.")


def potential_members(request: HttpRequest, club_pk: int) -> HttpResponse:
    club = Club.objects.get(pk=club_pk)
    players = club.potential_members.all()
    context = {
        'club': club,
        'players': players,
    }
    return render(request, 'clubs/club_potential_members.html', context)


def add_potential_club_member_to_real_members(request: HttpRequest, club_pk: int, player_pk: int) -> JsonResponse:
    response_data = {}
    club = get_object_or_404(Club, pk=club_pk, owner=request.user)
    player = get_object_or_404(Player, pk=player_pk)
    if player in club.potential_members.all():
        club.members.add(player)
        club.potential_members.remove(player)
        message = f"Поздравляем! Вам одобрили членство в клубе ---{club.name}---"
        notify.send(sender=club.owner, recipient=player, verb=message, target=club)
        response_data['success'] = True
        return JsonResponse(response_data)
    raise Http404("There is no potential players in the club")


def reject_potential_member(request: HttpRequest, club_pk: int, player_pk: int) -> JsonResponse:
    response_data = {}
    club = get_object_or_404(Club, pk=club_pk, owner=request.user)
    player = get_object_or_404(Player, pk=player_pk)
    if player in club.potential_members.all():
        club.potential_members.remove(player)
        message = f"Ваша заявка на членство в клубе ---{club.name}--- была отклонена."
        notify.send(sender=club.owner, recipient=player, verb=message, target=club)
        response_data['success'] = True
        return JsonResponse(response_data)
    raise Http404("There is no potential players in the club")


def potential_club_news_list(request: HttpRequest, club_pk: int) -> HttpResponse:
    club = Club.objects.get(pk=club_pk)
    news = News.objects.filter(club=club, is_published=News.PUBLISHED.NO, publishing_decision__isnull=True)
    context = {
        'club': club,
        'news': news,
    }
    return render(request, 'clubs/club_potential_news.html', context)


class PotentialClubNewsDetailView(ClubNewsDetailView):

    def get_queryset(self):
        club_pk = self.kwargs.get('club_pk')
        news_pk = self.kwargs.get('pk')
        club = Club.objects.get(pk=club_pk)
        if self.request.user != club.owner:
            raise Http404("You are not club owner!")
        return News.objects.select_related('club', 'author'). \
            filter(pk=news_pk, club=club, is_published=News.PUBLISHED.NO)


def add_potential_club_news(request: HttpRequest, club_pk: int, news_pk: int) -> JsonResponse:
    response_data = {}
    club = get_object_or_404(Club, pk=club_pk, owner=request.user)
    news = get_object_or_404(News, pk=news_pk)
    news.publishing_decision = News.DECISION.PUBLISH
    news.is_published = News.PUBLISHED.YES
    news.save()
    message = f"Ваша новость ---{news.name}--- опубликована."
    notify.send(sender=club.owner, recipient=news.author, verb=message, target=news)
    response_data['success'] = True
    return JsonResponse(response_data)


def reject_potential_club_news(request: HttpRequest, club_pk: int, news_pk: int) -> JsonResponse:
    response_data = {}
    club = get_object_or_404(Club, pk=club_pk, owner=request.user)
    news = get_object_or_404(News, pk=news_pk)
    news.publishing_decision = News.DECISION.REJECT
    news.save()
    message = f'Ваша новость "{news.name}" отклонена.'
    notify.send(sender=club.owner, recipient=news.author, verb=message, target=news)
    response_data['success'] = True
    return JsonResponse(response_data)