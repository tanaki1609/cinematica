from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializer, FilmDetailSerializer


@api_view(['GET'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Film not found!'})
    data = FilmDetailSerializer(film, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def film_list_api_view(request):
    # step 1: Collect films from DB (QuerySet)
    films = Film.objects.select_related('director').prefetch_related('reviews', 'genres').all()

    # step 2: Serialize queryset to list of dictionaries
    data = FilmListSerializer(films, many=True).data

    # step 3: Return response
    return Response(
        data=data,  # dictionary, list, list of dictionaries
        status=status.HTTP_200_OK  # status = int
    )
