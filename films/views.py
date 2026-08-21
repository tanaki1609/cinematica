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
        return Response(data={'error': 'Film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = FilmDetailSerializer(film, many=False).data
    return Response(data=data)


@api_view(['GET'])
def film_list_api_view(request):
    # step 1: Collect films (QuerySet)
    films = Film.objects.all()

    # step 2: Reformat QuerySet to list dictionary (Serializer)
    list_ = FilmListSerializer(films, many=True).data

    # step 3: Return response
    return Response(
        status=status.HTTP_200_OK,  # default (200) -> int
        data=list_  # str, int, bool, dict, list
    )
