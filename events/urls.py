from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='events'),
    path('my_events/', views.MyEventListView.as_view(), name='my_events'),
    path('event/<int:event_pk>/', views.show_event, name='event'),
    path('join_the_club/<int:event_pk>/', views.join_the_club, name='join_the_club'),
    path('search_partner/', views.get_search_partner_page, name='search_partner'),
    path('create_event/', views.EventCreationView.as_view(), name='create_event'),
    path('update_event/<int:pk>/', views.update_event, name='update_event'),
    path('invite_to_play/<int:player_pk>/', views.invite_to_play, name='invite_to_play'),
    path('reject_invitation/<int:invitation_pk>/<int:player_pk>/', views.reject_invitation, name='reject_invitation'),
    path('accept_invitation/<int:invitation_pk>/', views.accept_invitation, name='accept_invitation'),

    ]

