from django.urls import path
from . import views

app_name = 'additions'

urlpatterns = [
    path('', views.get_additions_index_page, name='index'),
]