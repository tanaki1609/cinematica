from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import (FilmListSerializer,
                          FilmDetailSerializer,
                          FilmValidateSerializer)


@api_view(['GET', 'PUT', 'DELETE'])  # GET->retrieve, PUT->update, DELETE->destroy
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Film not found!'})
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        film.title = serializer.validated_data.get('title')
        film.text = serializer.validated_data.get('text')
        film.rating_kp = serializer.validated_data.get('rating_kp')
        film.is_active = serializer.validated_data.get('is_active')
        film.director_id = serializer.validated_data.get('director_id')
        film.genres.set(serializer.validated_data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])  # GET->list, POST->create
def film_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect films from DB (QuerySet)
        films = Film.objects.select_related('director').prefetch_related('reviews', 'genres').all()

        # step 2: Serialize queryset to list of dictionaries
        data = FilmListSerializer(films, many=True).data

        # step 3: Return response
        return Response(
            data=data,  # dictionary, list, list of dictionaries
            status=status.HTTP_200_OK  # status = int
        )
    elif request.method == 'POST':
        # step 0: Validation (Existing, Typing, Extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        # step 1: Receive data from ValidatedData
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        rating_kp = serializer.validated_data.get('rating_kp')
        is_active = serializer.validated_data.get('is_active')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        # step 2: Create film by received data
        film = Film.objects.create(
            title=title,
            text=text,
            rating_kp=rating_kp,
            is_active=is_active,
            director_id=director_id
        )
        film.genres.set(genres)
        film.save()

        # step 3: Return response (status=201, data=optional)
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
