from django.contrib import admin
from .models import SingleTournament, DoublesTournament, TeamTournament


@admin.register(SingleTournament)
class SingleTournamentAdmin(admin.ModelAdmin):
    pass


@admin.register(DoublesTournament)
class DoublesTournamentAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamTournament)
class TeamTournamentAdmin(admin.ModelAdmin):
    pass
