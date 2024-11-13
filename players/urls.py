from django.urls import path
from . import views

app_name = 'players'

urlpatterns = [
    path('', views.get_players_index_page, name='index'),
    path('player_info/<slug:username>/', views.get_player_info, name='player_info'),
    path('plot_rating_data/<slug:username>/', views.plot_rating_graph, name='plot_rating_data'),
    # path('change_rating/', views.change_rating, name='change_rating'),
    path('registration/', views.register_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('notifications/', views.AllNotificationListView.as_view(), name='notifications'),
    path('notifications/invitation/', views.InvitationNotificationListView.as_view(), name='invitation_notifications'),
    path('notifications/events/', views.EventNotificationListView.as_view(), name='event_notifications'),
    path('notifications/clubs/', views.ClubNotificationListView.as_view(), name='clubs_notifications'),
    path('notifications/news/', views.NewsNotificationListView.as_view(), name='news_notifications'),
    path('notifications/actions/', views.NotificationActions.as_view(), name='notifications_actions'),

    path('validate_email/', views.validate_email, name='validate_email'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_password_view/', views.validate_password_view, name='validate_password_view'),

    # path('api/v1/players_list/', views.PlayersInfoAPIView.as_view(), name='api_players_list'),
    path('api/v1/api_players_rating/', views.PlayersRatingAPIView.as_view(), name='api_players_rating'),
]