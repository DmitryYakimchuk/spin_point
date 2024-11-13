from django.contrib import admin
from .models import News, NewsComment, NewsLike


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsLike)
class NewsLikeAdmin(admin.ModelAdmin):
    pass
