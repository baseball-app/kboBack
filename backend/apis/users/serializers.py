from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=255)
    nickname = serializers.CharField(max_length=255)
    my_team_id = serializers.IntegerField(write_only=True)
    my_team = serializers.SerializerMethodField()
    profile_image = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "email", "nickname", "my_team", "profile_image"]

    def get_my_team(self, obj):
        return obj

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSignUpInputSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    nickname = serializers.CharField()
    my_team = serializers.IntegerField()
