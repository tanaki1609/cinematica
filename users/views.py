from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterValidateSerializer


@api_view(['POST'])
def registration_api_view(request):
    # step 1: validation
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 2: receive data
    username = request.data.get('username')
    password = request.data.get('password')

    # step 3: create user
    user = User.objects.create_user(username=username, password=password)

    # step 4: return response
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})
