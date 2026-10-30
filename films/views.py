from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmSerializer, FilmDetailSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(data={'error': 'film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
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
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def film_list_create_api_view(request):
    if request.method == 'GET':
        # step 1: collect films (QuerySet)
        films = Film.objects.select_related('director').prefetch_related('genres').all()

        # step 2: reformat data (Serialize)
        list_ = FilmSerializer(films, many=True).data

        # step 3: return response
        return Response(data=list_)
    elif request.method == 'POST':
        # step 1: receive data (RequestBody)
        title = request.data.get('title')
        text = request.data.get('text')
        rating = request.data.get('rating')
        release_year = request.data.get('release_year')
        is_hit = request.data.get('is_hit')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

        # step 2: create film
        film = Film.objects.create(
            title=title,
            text=text,
            rating=rating,
            release_year=release_year,
            is_hit=is_hit,
            director_id=director_id,
        )
        film.genres.set(genres)

        # step 3: return response (film)
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
