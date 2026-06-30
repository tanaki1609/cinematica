from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializer, FilmDetailSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(data={'error': 'film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.release_year = request.data.get('release_year')
        film.rating = request.data.get('rating')
        film.is_hit = request.data.get('is_hit')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def film_list_create_api_view(request):
    if request.method == 'GET':
        # step 1: collect films (QuerySet)
        films = (Film.objects.select_related('director')
                 .prefetch_related('genres', 'reviews').all())

        # step 2: reformat QuerySet to list of dictionary (Serializer)
        list_ = FilmListSerializer(films, many=True).data

        # step 3: return response
        return Response(
            data=list_
        )
    elif request.method == 'POST':
        # step 1: receive data from request body
        title = request.data.get('title')
        text = request.data.get('text')
        release_year = request.data.get('release_year')
        is_hit = request.data.get('is_hit')
        rating = request.data.get('rating')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

        # step 2: create film
        film = Film.objects.create(
            title=title,
            text=text,
            release_year=release_year,
            is_hit=is_hit,
            rating=rating,
            director_id=director_id,
        )
        film.genres.set(genres)
        film.save()

        # step 3: return response (status, data[optional])
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
