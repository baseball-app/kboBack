from django.shortcuts import render
from rest_framework.test import APITestCase, APIClient

from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model

from users.models import User
from games.models import Team
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
            'email' : data.get('email'),
            'nickname' : data.get('nickname'),
        },status = status.HTTP_201_CREATED)

class UpdateMyTeamApi(APIView):
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user == request.user:
                team_id = request.data.get('team_id')
                if team_id:
                    try:
                        team = Team.objects.get(pk=team_id)
                        user.my_team = team
                        user.save()
                        return Response({"message": "Team updated successfully"}, status=status.HTTP_200_OK)
                    except Team.DoesNotExist:
                        return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error": "Team ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(APIView):
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user == request.user:
                current_password = request.data.get('current_password')
                new_password = request.data.get('new_password')

                if current_password and new_password:
                    if authenticate(username=user.email, password=current_password):
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)
                        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error": "Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Both current and new passwords are required"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


