from rest_framework import serializers
from rest_framework.serializers import Serializer


class NaverInputSerializer(Serializer):
    code = serializers.CharField(max_length=255, required=True)
    state = serializers.CharField(max_length=255, required=True)


class KakaoInputSerializer(Serializer):
    code = serializers.CharField(max_length=255, required=True)
    state = serializers.CharField(max_length=255, required=False)


class AppleInputSerializer(Serializer):
    code = serializers.CharField(max_length=255, required=True)
    state = serializers.CharField(max_length=255, required=False)


class TokenRefreshSerializer(Serializer):
    refresh_token = serializers.CharField(max_length=255, required=True)
