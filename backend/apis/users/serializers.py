from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apps.teams.models import UserTeam
from apps.users.models import Friendship


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


class UserInfoSerializer(Serializer):
    nickname = serializers.CharField(max_length=255)
    predict_ratio = serializers.SerializerMethodField()
    my_team = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    def get_predict_ratio(self, obj):
        # todo: tickets 관련 처리 후 작업
        return 1

    def get_my_team(self, obj):
        team = UserTeam.objects.get(user=obj).team
        return team.id

    def get_followers(self, obj):
        return list(Friendship.objects.filter(target=obj).values_list('source_id', flat=True))

    def get_followings(self, obj):
        return list(Friendship.objects.filter(source=obj).values_list('target_id', flat=True))


class UserLeaveSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserFollowSerializer(Serializer):
    source_id = serializers.IntegerField(required=True)
    target_id = serializers.IntegerField(required=True)


class UserInvitationSerializer(Serializer):
    code = serializers.CharField()
