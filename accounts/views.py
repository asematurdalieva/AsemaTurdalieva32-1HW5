from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import LoginValidateSerializer, SignUpValidateSerializer
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login_api_view(request):
    serializer = LoginValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'message': 'Successful authorization ',
                              'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'message': 'Unauthorized'})


@api_view(['POST'])
def signup_api_view(request):
    serializer = SignUpValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    validated_data['is active'] = False
    user = User.objects.create_user(**serializer.validated_data)
    return Response(data={'message': 'User created', 'user_id': user.id})


@api_view(['GET'])
def confirm_user_api_view(request, userid):
    user = get_object_or_404(User, id=userid)
    user.is_active = True
    user.save()
    return Response(data={'message': 'User confirmed successfully.'})
