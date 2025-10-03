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
        return Response(data={'error': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = FilmDetailSerializer(film, many=False).data
    return Response(data=data)


@api_view(['GET'])
def film_list_api_view(request):
    # step 1: Collect data (QuerySet)
    films = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()

    # step 2: Reformat queryset to list of dictionary
    data = FilmListSerializer(films, many=True).data

    # step 3: Return Response
    return Response(data=data, status=status.HTTP_200_OK)
