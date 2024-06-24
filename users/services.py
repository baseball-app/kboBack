from users.models import User
from games.models import Team
from users.selectors import UserSelector
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserService:
    def __init__(self):
        pass

    def sign_up(self, email: str, password: str, nickname: str, my_team: int):
        team = Team.objects.get(id = my_team)
        user = User(
            email = email,
            nickname = nickname,
        )
        user.set_password(password)
        user.my_team = team
        user.save()

    def login(self, email: str, password: str):
        selector = UserSelector()

        user = selector.get_user_by_email(email)

        if not selector.check_password(user, password):
            raise exceptions.ValidationError(
                {'detail': "아이디나 비밀번호가 올바르지 않습니다."}
            )
        
        token = RefreshToken.for_user(user=user)

        data = {
            'email': user.email,
            'refresh': str(token),
            'access': str(token.access_token),
            'nickname': user.nickname,
        }

        return data