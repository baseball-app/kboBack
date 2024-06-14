from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from users.models import User
from users.services import UserService


class SignUpApi(APIView):
    permission_classes = (AllowAny, )

    class SignUpInputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        nickname = serializers.CharField()
        my_team = serializers.CharField()

    def post(self, request):
        serializer = self.SignUpInputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_service = UserService()

        user_service.sign_up(
            email = data.get('email'),
            password = data.get('password'),
            nickname = data.get('nickname'),
            my_team = data.get('my_team'),
        )
        return Response({
            'status': 'success',
        },status = status.HTTP_201_CREATED)
