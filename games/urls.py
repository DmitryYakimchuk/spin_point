from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.get_games_index_page, name='index'),
    path('tournaments/', views.get_tournaments, name='tournaments'),
]