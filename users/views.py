from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserAuthSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )
    # create code (6-symbol) -> user
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']  # admin
    password = serializer.validated_data['password']  # 123

    user = authenticate(username=username, password=password)  # user/None
    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
