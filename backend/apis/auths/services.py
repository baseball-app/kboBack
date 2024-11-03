import requests

from apps.auths.models import SocialInfo
from apps.users.models import User
from django.conf import settings


class AuthService:
    def get_user_info(self):
        pass

    def get_access_token(self, code: str, state: str):
        pass

    def get_user_info(self, access_token: str):
        pass


class NaverAuthService(AuthService):
    def get_social_user(self, data):
        access_token = self._get_access_token(data)
        if not access_token:
            return None

        user_info = self._get_user_info(access_token)
        if not user_info:
            return None

        social = SocialInfo.objects.filter(social_id=user_info["id"]).last()
        if not social:
            return None

        user = User.objects.filter(social_id=social.user_id).last()
        if not user:
            return None

        return user

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
        access_token = self._get_access_token(data)
        if not access_token:
            return None

        user_info = self._get_user_info(access_token)
        if not user_info:
            return None

        return user_info

    def get_user(self, data):
        access_token = self._get_access_token(data)
        if not access_token:
            return None

        user_info = self._get_user_info(access_token)
        if not user_info:
            return None

        social = SocialInfo.objects.filter(social_id=user_info["id"]).last()
        if not social:
            return None

        user = User.objects.filter(id=social.user_id).last()
        if not user:
            return None

        return user

    def _get_access_token(self, data):
        grant_type = "authorization_code"
        redirect_uri = "http://localhost:8000/auths/kakao/callback"
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
