from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.get_tournaments_index_page, name='index'),
]