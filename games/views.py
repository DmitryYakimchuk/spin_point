from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def get_games_index_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'games/index.html', {})


def get_tournaments(request: HttpRequest) -> HttpResponse:
    return render(request, 'games/tournaments.html', {})
