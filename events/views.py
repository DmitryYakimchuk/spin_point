import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Subquery, Q
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView
from notifications.signals import notify

from events.forms import EventCreationForm
from events.models import Invitation, Event
from players.models import Player
from utils.players_filters import get_filtered_players


@login_required(login_url="players:login")
def get_search_partner_page(request: HttpRequest) -> HttpResponse:
    """Function is similar to get_players_index_page, but has addition filter:
    if player is available to searching"""

    form, players = get_filtered_players(request)
    players = players.filter(searchable=Player.SEARCHABLE.YES).exclude(pk=request.user.pk)
    filtered_invitations = Invitation.objects.filter(initiator=request.user, invited__in=Subquery(players.values('pk')),
                                                     created_at__day=datetime.today().day
                                                     )
    players = players.exclude(pk__in=Subquery(filtered_invitations.values('invited_id'))).order_by('position'). \
        select_related('city')
    players_count = players.count()

    # Show 5 players per page
    paginator = Paginator(players, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'search_partner_page': True,
        'players_count': players_count,
    }
    return render(request, 'events/search_partner.html', context)


# @login_required
# def invite_to_play(request: HttpRequest, player_pk: int) -> HttpResponse | JsonResponse:
#     response_data = {}
#     player = get_object_or_404(Player, pk=player_pk, searchable=Player.SEARCHABLE.YES)
#     if request.user != player:
#         # A player can only invite another player once per day
#         if not Invitation.objects.filter(initiator=request.user, invited=player, created_at__day=datetime.today().day). \
#                 exists():
#             message = f'{request.user} приглашает Вас вместе поиграть.'
#             invitation = Invitation.objects.create(initiator=request.user, invited=player,
#                                                    status=Invitation.STATUS.ACTIVE)
#             notify.send(sender=request.user, recipient=player, verb=message, target=invitation)
#             response_data['success'] = True
#             response_data['html'] = r"<a id=\"invite-button\" href=\"/invite/{{ player.pk }}\"" \
#                                     r"class=\"btn btn-primary text-uppercase m-1\">Приглашение отправлено</a>"
#             return JsonResponse(response_data)
#         else:
#             response_data['error'] = 'Сегодня Вы уже приглашали этого игрока сыграть. Ожидайте его ответа.'
#             return JsonResponse(response_data)
#     else:
#         response_data['error'] = 'Вы не можете пригласить сами себя.'
#         return JsonResponse(response_data)


@login_required
def invite_to_play(request: HttpRequest, player_pk: int) -> JsonResponse:
    player = get_object_or_404(Player, pk=player_pk, searchable=Player.SEARCHABLE.YES)
    if request.user != player:
        # Проверяем, что текущий пользователь еще не приглашал данного игрока сегодня
        if not Invitation.objects.filter(initiator=request.user, invited=player,
                                         created_at__day=datetime.today().day).exists():
            # Создаем приглашение и отправляем уведомление
            message = f'Вас приглашает вместе поиграть '
            invitation = Invitation.objects.create(initiator=request.user, invited=player,
                                                   status=Invitation.STATUS.ACTIVE)
            notify.send(sender=request.user, recipient=player, verb=message, target=invitation)
            response_data = {'success': True}
            return JsonResponse(response_data)
        else:
            response_data = {'error': 'Сегодня Вы уже приглашали этого игрока.'}
            return JsonResponse(response_data)
    else:
        response_data = {'error': 'Вы не можете пригласить сами себя.'}
        return JsonResponse(response_data)


@login_required
def reject_invitation(request: HttpRequest, invitation_pk: int, player_pk: int) -> JsonResponse:
    player = get_object_or_404(Player, pk=player_pk)
    if request.user != player:
        invitation = get_object_or_404(Invitation, pk=invitation_pk, initiator=player, invited=request.user,
                                       status=Invitation.STATUS.ACTIVE)
        invitation.status = Invitation.STATUS.REJECTED
        invitation.save()
        rejection_reason = request.POST.get('rejection_reason', None)  # Получаем причину отказа из запроса
        rejection_reason = rejection_reason.strip()
        response_message = f'Ваше приглашение сегодня было отклонено игроком '
        own_message = f'Вы отклонили приглашение '
        if rejection_reason:
            notify.send(sender=request.user, recipient=player, verb=response_message, target=invitation,
                        description=rejection_reason)
            notify.send(sender=player, recipient=request.user, verb=own_message, target=invitation,
                        description=rejection_reason)
        else:
            notify.send(sender=request.user, recipient=player, verb=response_message, target=invitation)
            notify.send(sender=player, recipient=request.user, verb=own_message, target=invitation)
        response_data = {'success': True}
        return JsonResponse(response_data)
    else:
        raise Http404("Такой страницы не существует :(")


@login_required
def accept_invitation(request: HttpRequest, invitation_pk: int) -> JsonResponse:
    invitation = get_object_or_404(Invitation, pk=invitation_pk, invited=request.user, status=Invitation.STATUS.ACTIVE)
    invitation.status = Invitation.STATUS.ACCEPTED
    event_name = f'{invitation.initiator.username} VS {invitation.invited.username}'
    event = Event.objects.create(name=event_name, initiator=invitation.initiator, is_open=Event.OPEN.NO)
    event.allowed_participants.add(invitation.initiator, invitation.invited)
    event.participants.add(invitation.initiator, invitation.invited)

    message_to_initiator = f'{invitation.invited.username} принял Ваше приглашение. Ваша общая встреча уже создана.' \
                           f'Вы являетесь её инициатором и только Вы можете вносить информацию о встрече.'
    notify.send(sender=invitation.invited, recipient=invitation.initiator, verb=message_to_initiator, target=event)
    message_to_invited = f'Вы приняли приглашение {invitation.initiator.username}. Ваша общая встреча уже создана.' \
                         f'Вы можете писать комментарии к этой встрече, однако вносить изменения по информации о ' \
                         f'встрече может только её инициатор.'
    notify.send(sender=invitation.initiator, recipient=invitation.initiator, verb=message_to_invited, target=event)

    return redirect('events:event', event_pk=event.pk)


@login_required
def show_event(request: HttpRequest, event_pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=event_pk)
    context = {
        'event': event,
    }
    return render(request, 'events/event.html', context)


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    paginate_by = 10
    context_object_name = 'events'
    extra_context = {
        'title': 'События',
    }

    def get_queryset(self):
        return Event.objects.filter(Q(is_open=Event.OPEN.YES) |
                                    Q(initiator=self.request.user) |
                                    Q(participants__in=[self.request.user]) |
                                    Q(allowed_participants__in=[self.request.user])). \
            order_by('-created_at'). \
            select_related('city', 'club', 'initiator'). \
            prefetch_related('participants', 'allowed_participants')


class MyEventListView(EventListView):
    extra_context = {
        'title': 'Мои события',
    }

    def get_queryset(self):
        return Event.objects.filter(Q(participants__in=[self.request.user])). \
            order_by('-created_at'). \
            select_related('city', 'club', 'initiator'). \
            prefetch_related('participants', 'allowed_participants')


class EventCreationView(LoginRequiredMixin, CreateView):
    """Creating the event and automatically adding user to initiator, allowed_participants and participants fields"""

    model = Event
    form_class = EventCreationForm
    template_name = 'events/create_event.html'
    login_url = reverse_lazy('players:login')
    success_url = reverse_lazy('events:my_events')
    extra_context = {
        'title': 'Создание нового события',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Because of members is ManyToMany field
         we cannot save object with value player to members simultaneously.
         At the first step we create and save Event object with empty participants and allowed_participants filed.
         And then we can add the initiator to participants and allowed_participants list"""

        event = form.save(commit=False)
        initiator = Player.objects.get(username=self.request.user.username)
        event.initiator = initiator
        event.save()
        event.participants.add(initiator)
        event.allowed_participants.add(initiator)
        return super().form_valid(form)


@login_required(login_url=reverse_lazy('players:login'))
def update_event(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.initiator:
        return redirect('events:my_events')

    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event', event_pk=event.pk)
    else:
        form = EventCreationForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'title': 'Редактирование события',
        'update': True,
    }

    return render(request, 'events/create_event.html', context)


def join_the_club(request: HttpRequest, event_pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=event_pk)
    if event.is_open and request.user not in event.participants.all():
        event.participants.add(request.user)
        message_to_initiator = f' присоединился к Вашему событию: '
        notify.send(sender=request.user, recipient=event.initiator, verb=message_to_initiator, target=event)
        return redirect('events:event', event_pk=event.pk)
    else:
        raise Http404("Такой страницы не существует :(")