from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apis.teams.serializers import TeamsSerializer
from apps.teams.models import UserTeam
from apps.users.models import Friendship

User = get_user_model()


class UserSimpleSerializer(ModelSerializer):
    id = serializers.IntegerField()
    nickname = serializers.CharField()
    profile_type = serializers.IntegerField()
    profile_image = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "nickname", "profile_type", "profile_image"]


class UserModifySerializer(Serializer):
    nickname = serializers.CharField(max_length=255, required=False)
    my_team = serializers.IntegerField(required=False)
    profile_type = serializers.IntegerField(required=False)
    profile_image = serializers.CharField(max_length=255, required=False)


class UserInfoSerializer(Serializer):
    nickname = serializers.CharField()
    profile_type = serializers.IntegerField()
    profile_image = serializers.SerializerMethodField()
    predict_ratio = serializers.SerializerMethodField()
    my_team = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        return f"{settings.AWS_S3_CUSTOM_DOMAIN}{obj.profile_image}" if obj.profile_image else ""

    def get_predict_ratio(self, obj):
        # todo: tickets 관련 처리 후 작업
        return 1

    def get_my_team(self, obj):
        user_team = UserTeam.objects.filter(user=obj).last()
        return TeamsSerializer(user_team.team).data if user_team else {}

    def get_followers(self, obj):
        return len(Friendship.objects.filter(target=obj).values_list("source_id", flat=True))

    def get_followings(self, obj):
        return len(Friendship.objects.filter(source=obj).values_list("target_id", flat=True))


class UserFollowSerializer(Serializer):
    source_id = serializers.IntegerField(required=True)
    target_id = serializers.IntegerField(required=True)


class UserFollowersSerializer(Serializer):
    followers = serializers.SerializerMethodField()

    def get_followers(self, obj):
        friendships = Friendship.objects.filter(target=obj).prefetch_related(
            Prefetch("source", queryset=User.objects.all())
        )
        return UserSimpleSerializer([friendship.source for friendship in friendships], many=True).data


class UserFollowingsSerializer(Serializer):
    followings = serializers.SerializerMethodField()

    def get_followings(self, obj):
        friendships = Friendship.objects.filter(source=obj).prefetch_related(
            Prefetch("target", queryset=User.objects.all())
        )
        return UserSimpleSerializer([friendship.target for friendship in friendships], many=True).data


class UserInvitationSerializer(Serializer):
    code = serializers.CharField()
