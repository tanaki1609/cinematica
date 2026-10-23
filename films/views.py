from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmSerializer, FilmDetailSerializer


@api_view(['GET'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(data={'error': 'film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = FilmDetailSerializer(film, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def film_list_api_view(request):
    # step 1: collect films (QuerySet)
    films = Film.objects.all()

    # step 2: reformat data (Serialize)
    list_ = FilmSerializer(films, many=True).data

    # step 3: return response
    return Response(data=list_)
