from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.get_news_index_page, name='index'),
    path('rules', views.get_rules, name='rules'),
    path('about_us', views.about_us, name='about_us'),
    path('news', views.PublicNewsListView.as_view(), name='public_news_list'),
    path('news/<int:pk>/', views.PublicNewsDetailView.as_view(), name='get_the_open_news'),
    path('creating_news/', views.NewsCreationView.as_view(), name='creating_news'),
    path('updating_news/<int:pk>/', views.UpdateNewsView.as_view(), name='updating_news'),
    path('like_news/<int:news_pk>/', views.like_news, name='like_news'),
]