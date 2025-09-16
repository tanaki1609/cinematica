from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterValidateSerializer, AuthValidateSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_api_view(request):
    # step 0: Validation
    serializer = RegisterValidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'errors': serializer.errors})

    # step 1: Create user
    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        is_active=False
    )
    # code (6-symbol) -> user

    # step 2: Return response
    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id})


@api_view(['POST'])
def authorization_api_view(request):
    # step 0: Validation
    serializer = AuthValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 1: Authentication
    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password']
    )

    # step 2: Return Token (get or create)
    if user is not None:
        try:
            token_ = Token.objects.get(user=user)
        except:
            token_ = Token.objects.create(user=user)
        return Response(data={'key': token_.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
