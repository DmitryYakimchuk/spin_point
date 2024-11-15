"""
URL configuration for ttennis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', include('news.urls', namespace='news')),
    path('players/', include('players.urls', namespace='players')),
    path('events/', include('events.urls', namespace='events')),
    path('games/', include('games.urls', namespace='games')),
    path('clubs/', include('clubs.urls', namespace='clubs')),
    path('additions/', include('additions.urls', namespace='additions')),
    path('tournaments/', include('tournaments.urls', namespace='tournaments')),
]


# For debug_toolbar
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]

# For media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
