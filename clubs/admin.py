from django.contrib import admin
from .models import Club, ClubReview


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    pass


@admin.register(ClubReview)
class ClubReviewAdmin(admin.ModelAdmin):
    pass
