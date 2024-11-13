from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path('', views.ClubList.as_view(), name='index'),
    path('club/<int:pk>/', views.ClubView.as_view(), name='club'),
    path('club/<int:club_pk>/news_list/', views.ClubNewsListView.as_view(), name='club_list_news'),
    path('club/<int:club_pk>/news/<int:pk>/', views.ClubNewsDetailView.as_view(), name='club_news'),
    path('club/<int:pk>/players/', views.ClubPlayersList.as_view(), name='club_players'),
    path('create/', views.ClubCreationView.as_view(), name='create_club'),
    path('edit_club/<int:pk>/', views.UpdateClubView.as_view(), name='edit_club'),
    path('my_clubs/', views.MyClubList.as_view(), name='my_clubs'),
    path('participation_in_clubs/', views.ParticipationClubList.as_view(), name='participation_in_clubs'),
    path('add_potential_members/<int:club_pk>/', views.add_player_to_potential_club_members, name='add_potential_members'),
    path('potential_members/<int:club_pk>/', views.potential_members, name='potential_members'),
    path('add_to_open_club_members/<int:club_pk>/', views.add_to_open_club_members, name='add_to_open_club_members'),
    path('to_real_members/<int:club_pk>/<int:player_pk>/', views.add_potential_club_member_to_real_members, name='to_real_members'),
    path('reject_potential_member/<int:club_pk>/<int:player_pk>/', views.reject_potential_member, name='reject_potential_member'),
    path('potential_club_news_list/<int:club_pk>/', views.potential_club_news_list, name='potential_club_news_list'),
    path('potential_club_news/<int:club_pk>/<int:pk>/', views.PotentialClubNewsDetailView.as_view(), name='potential_club_news'),
    path('to_club_news/<int:club_pk>/<int:news_pk>/', views.add_potential_club_news, name='to_club_news'),
    path('reject_club_news/<int:club_pk>/<int:news_pk>/', views.reject_potential_club_news, name='reject_club_news'),
]