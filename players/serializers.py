from rest_framework import serializers
from .models import Player, Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('rating_date', 'rating')


class PlayersRatingSerializer(serializers.ModelSerializer):
    rating_player = RatingSerializer(read_only=True, many=True)

    class Meta:
        model = Player
        fields = ('username', 'rating_player')
