from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Director
from .serializers import (
    FilmListSerializer,
    FilmDetailSerializer,
    FilmValidateSerializer
)
from django.db import transaction


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
    else:
        serializer = FilmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film.title = serializer.validated_data.get('title')
        film.text = serializer.validated_data.get('text')
        film.rating = serializer.validated_data.get('rating')
        film.release_year = serializer.validated_data.get('release_year')
        film.is_hit = serializer.validated_data.get('is_hit')
        film.director_id = serializer.validated_data.get('director_id')
        film.genres.set(serializer.validated_data.get('genres'))
        film.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=FilmDetailSerializer(film).data
        )


@api_view(['GET', 'POST'])
def film_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: collect films (QuerySet)
        films = (Film.objects.select_related('director')
                 .prefetch_related('genres', 'reviews').all())

        # step 2: reformat films to list of dictionary
        data = FilmListSerializer(films, many=True).data

        # step 3: return response
        return Response(
            data=data,  # dictionary, list
            status=status.HTTP_200_OK,  # status = 100, 200, 300, 400, 500
        )
    elif request.method == 'POST':
        # step 0: Validation (Existing, Typing, Extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Receive data
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        rating = serializer.validated_data.get('rating')
        release_year = serializer.validated_data.get('release_year')
        is_hit = serializer.validated_data.get('is_hit')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        # step 2: Create film by received data
        with transaction.atomic():
            film = Film.objects.create(
                title=title,
                text=text,
                rating=rating,
                release_year=release_year,
                is_hit=is_hit,
                director_id=director_id,
            )
            film.genres.set(genres)
            film.save()

        # step 3: Return Response
        return Response(
            status=status.HTTP_201_CREATED,
            data=FilmDetailSerializer(film).data
        )
