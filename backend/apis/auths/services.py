import requests
from django.conf import settings
from django.db import transaction

from apps.auths.chocies import SocialTypeEnum
from apps.auths.models import SocialInfo
from apps.users.models import User

import logging

logger = logging.getLogger(__name__)


class AuthService:
    def _get_access_token(self, data):
        pass

    def _get_user_info(self, access_token: str):
        pass


class NaverAuthService(AuthService):
    def get_social_user(self, data):
        access_token = self._get_access_token(data)
        if not access_token:
            return None
        return self._get_user_info(access_token)

    def auth_or_register(self, social_user_info):
        social_id = social_user_info["id"]

        # 기존 유저 조회
        social_info = SocialInfo.objects.filter(social_id=social_id).last()
        if social_info:
            user = User.objects.filter(id=social_info.user_id).last()
            if not user:
                return None, None
            return user, False

        # 신규 유저 생성
        with transaction.atomic():
            user = User.objects.create(nickname=f"naver_{social_id}")
            SocialInfo.objects.create(user=user, social_id=social_id, type=SocialTypeEnum.NAVER.value)

        return user, True

    def _get_access_token(self, data):
        grant_type = "authorization_code"
        client_id = settings.SOCIAL_LOGIN.get("NAVER").get("CLIENT_ID")
        client_secret = settings.SOCIAL_LOGIN.get("NAVER").get("CLIENT_SECRET")
        code = data.get("code")
        state = data.get("state")
        response = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type={grant_type}&code={code}&state={state}"
            f"&client_id={client_id}&client_secret={client_secret}"
        ).json()
        access_token = response.get("access_token", None)
        return access_token

    def _get_user_info(self, access_token: str):
        response = requests.post(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()
        message = response.get("message", "failed")
        return response["response"] if message == "success" else None


class KakaoAuthService(AuthService):
    def get_social_user(self, data):
        try:
            access_token = self._get_access_token(data)
            if not access_token:
                return None
            return self._get_user_info(access_token)
        except Exception as e:
            logger.error(f"Failed to get social user info: {str(e)}")
            return None

    def auth_or_register(self, social_user_info):
        try:
            social_id = social_user_info["id"]

            # 기존 유저 조회
            social_info = SocialInfo.objects.filter(social_id=social_id).last()
            if social_info:
                user = User.objects.filter(id=social_info.user_id).last()
                if not user:
                    return None, None
                return user, False

            # 신규 유저 생성
            with transaction.atomic():
                user = User.objects.create(nickname=f"kakao_{social_id}")
                SocialInfo.objects.create(user=user, social_id=social_id, type=SocialTypeEnum.KAKAO.value)

            return user, True
        except Exception as e:
            logger.error(f"Failed to authenticate or register user: {str(e)}")
            return None, None


    def _get_access_token(self, data):
        grant_type = "authorization_code"
        redirect_uri = f"{settings.DEFAULT_HOST}/auths/kakao/callback"
        client_id = settings.SOCIAL_LOGIN.get("KAKAO").get("CLIENT_ID")
        client_secret = settings.SOCIAL_LOGIN.get("KAKAO").get("CLIENT_SECRET")
        code = data.get("code")
        response = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type={grant_type}&code={code}&redirect_uri={redirect_uri}"
            f"&client_id={client_id}&client_secret={client_secret}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        ).json()
        access_token = response.get("access_token", None)
        return access_token

    def _get_user_info(self, access_token: str):
        response = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer {access_token}",
            },
        ).json()
        return response if response["id"] else None
