from django.contrib import admin
from .models import SingleGame, DoublesGame, TeamGame


@admin.register(SingleGame)
class SingleGameAdmin(admin.ModelAdmin):
    pass


@admin.register(DoublesGame)
class DoublesGameAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamGame)
class TeamGameAdmin(admin.ModelAdmin):
    pass
