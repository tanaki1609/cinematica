from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import (FilmListSerializer,
                          FilmDetailSerializer,
                          FilmValidateSerializer)


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.rating = request.data.get('rating')
        film.release_year = request.data.get('release_year')
        film.is_hit = request.data.get('is_hit')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)


@api_view(['GET', 'POST'])
def film_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect all films (QuerySet)
        films = (Film.objects.select_related('director')
                 .prefetch_related('reviews', 'genres')
                 .all())

        # step 2: Reformat (Serialize) data (list of dictionaries)
        list_ = FilmListSerializer(films, many=True).data

        # step 3: Return Response
        return Response(data=list_,
                        status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # step 0: Validation (Existing, Typing, Extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Receive data
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        release_year = serializer.validated_data.get('release_year')
        rating = serializer.validated_data.get('rating')
        is_hit = serializer.validated_data.get('is_hit') # "Y"
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        # step 2: Create film
        with transaction.atomic():
            film = Film.objects.create(
                title=title,
                text=text,
                release_year=release_year,
                rating=rating,
                is_hit=is_hit,
                director_id=director_id
            )
            film.genres.set(genres)
            film.save()

        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
