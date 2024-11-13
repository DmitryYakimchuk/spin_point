from django.contrib import admin
from .models import Player, Rating, Doubles, Team, ChatMessage, SearchPartner


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_filter = ('player', 'rating_date', 'rating', 'created_at', 'updated_at')


@admin.register(Doubles)
class DoublesAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(SearchPartner)
class SearchPartnerAdmin(admin.ModelAdmin):
    pass
