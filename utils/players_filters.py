"""Here is the function for player's filters to get some statistics info"""
from datetime import datetime

from django.http import HttpRequest

from django.db import connection
from django.db import models
from django.db.models import Window, F, Subquery, Q, Max
from django.db.models.functions import DenseRank

from players.forms import PlayerFilterForm
from players.models import Player, Rating


def get_filtered_players(request: HttpRequest) -> tuple:
    # Taking latest rating and corresponding position for each player
    players = get_ordered_rating_and_position_players_queryset(Player.objects)
    # Saving positions for each player
    positions = {player.pk: player.position for player in players}

    # Filters part
    if request.method == 'GET':
        form = PlayerFilterForm(request.GET)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            sex = form.cleaned_data.get('sex')
            min_age = form.cleaned_data.get('min_age')
            max_age = form.cleaned_data.get('max_age')
            city = form.cleaned_data.get('city')
            club = form.cleaned_data.get('club')
            min_rating = form.cleaned_data.get('min_rating') if form.cleaned_data.get('min_rating') else 0
            max_rating = form.cleaned_data.get('max_rating') if form.cleaned_data.get('max_rating') else 10000
            has_photo = form.cleaned_data.get('has_photo')
            role = form.cleaned_data.get('role')
            skill_level = form.cleaned_data.get('skill_level')
            playstyle = form.cleaned_data.get('playstyle')
            hand = form.cleaned_data.get('hand')

            if username:
                players = players.filter(username__icontains=username)
            if sex != '':
                players = players.filter(sex=True if sex == '1' else False)
            if min_age:
                players = players.filter(birthday__year__lte=(datetime.now().year - min_age))
            if max_age:
                players = players.filter(birthday__year__gte=(datetime.now().year - max_age))
            if city:
                players = players.filter(city=city)
            if club:
                players = players.filter(club_members=club)
            if has_photo:
                players = players.exclude(photo='')
            if role:
                players = players.filter(role=role)
            if skill_level:
                players = players.filter(skill_level=skill_level)
            if playstyle:
                players = players.filter(playstyle=playstyle)
            if hand:
                players = players.filter(hand=hand)

            # Filter for latest rating
            players = players.annotate(
                max_rating_date=Max('rating_player__rating_date')
            ).filter(
                Q(rating_player__rating_date=models.Subquery(
                    Rating.objects.filter(
                        player_id=models.OuterRef('pk')
                    ).order_by('-created_at').values('rating_date')[:1]
                )) &
                Q(rating_player__rating__gte=min_rating) &
                Q(rating_player__rating__lte=max_rating)
            )

        # Getting back real positions for players after filtration
        for player in players:
            player.position = positions.get(player.pk, 'ошибка')

    else:
        form = PlayerFilterForm()

    #  Set age: REFACTOR USING F-function!
    for player in players:
        if player.birthday is not None:
            age = datetime.today().year - player.birthday.year - (
                    (datetime.today().month, datetime.today().day) < (player.birthday.month, player.birthday.day))
            player.age = age

    return form, players


def get_ordered_rating_and_position_players_queryset(players: Player) -> Player:
    #  annotate(
    #                 max_rating_date=Max('rating_player__rating_date')
    #             )
    return players.annotate(
        latest_rating=Subquery(
            Rating.objects.filter(
                player_id=models.OuterRef('pk')
            ).order_by('-created_at').values('rating')[:1]
        )
    ).annotate(
        position=Window(
            expression=DenseRank(),
            order_by=F('latest_rating').desc(),
        )).order_by('position')


def get_player_last_rating_position(username: str) -> int:
    """The function solves Django ORM problem to get rating position.
    Classical Django approach with corresponding code work almost good:
        window = Window(expression=Rank(), order_by=F('rating').desc())
        position = Player.objects.annotate(position=window)
    You will get all the data with proper rating positions.
    But when you would like to use .get(username=username) or .filter(username=username)
    you will get position == 1 for each object you used. It does not matter which rating really is.
    Raw query doesn't have this problem.
    """

    sql_query = f"""
         WITH players_rating as (SELECT 
                                       "players_player"."id",
                                       "players_player"."username",
                                       "players_player"."created_at",
                                       "players_player"."updated_at",
                                       (
                                        SELECT U0."rating"
                                          FROM "players_rating" U0
                                         WHERE U0."player_id" = ("players_player"."id")
                                         ORDER BY U0."created_at" DESC
                                         LIMIT 1
                                       ) AS "latest_rating",
                                       DENSE_RANK() OVER (ORDER BY (SELECT U0."rating" FROM "players_rating" U0 WHERE U0."player_id" = ("players_player"."id") ORDER BY U0."created_at" DESC LIMIT 1) DESC) AS "position"
                                FROM "players_player")	  
        SELECT position FROM players_rating WHERE username='{username}';
    """

    # Execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()

    return row[0]