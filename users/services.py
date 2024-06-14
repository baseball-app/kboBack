from users.models import User
from games.models import Team

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
