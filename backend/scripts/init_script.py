import toml
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application

from apps.teams.models import Team, UserTeam
from apps.users.models import Friendship
from conf.settings.base import BASE_DIR

User = get_user_model()
config = toml.load(BASE_DIR / "config.toml")


def make_auth():
    email = config["init"]["email"]
    nickname = config["init"]["nickname"]
    password = config["init"]["password"]

    default_user, _ = User.objects.get_or_create(
        email=email,
        nickname=nickname,
        password=password,
    )

    client_id = config["init"]["client_id"]
    client_secret = config["init"]["client_secret"]
    client_type = config["init"]["client_type"]
    authorization_grant_type = config["init"]["authorization_grant_type"]
    redirect_uris = config["init"]["redirect_uris"]

    try:
        Application.objects.get(client_id=client_id)
    except Application.DoesNotExist:
        Application.objects.create(
            name="dev",
            client_id=client_id,
            client_secret=client_secret,
            client_type=client_type,
            authorization_grant_type=authorization_grant_type,
            redirect_uris=redirect_uris,
            user_id=default_user.id,
        )


def make_users():
    users = [
        {"email": "user1@kboapp.com", "nickname": "user1", "password": "password1"},
        {"email": "user2@kboapp.com", "nickname": "user2", "password": "password2"},
        {"email": "user3@kboapp.com", "nickname": "user3", "password": "password3"},
    ]

    for user_data in users:
        User.objects.get_or_create(
            email=user_data["email"], defaults={"nickname": user_data["nickname"], "password": user_data["password"]}
        )


def make_teams():
    teams = [
        {"name": "KIA 타이거즈", "logo_url": "https://image.com/"},
        {"name": "삼성 라이온즈", "logo_url": "https://image.com/"},
        {"name": "LG 트윈스", "logo_url": "https://image.com/"},
        {"name": "두산 베어스", "logo_url": "https://image.com/"},
        {"name": "KT 위즈", "logo_url": "https://image.com/"},
        {"name": "SSG 랜더스", "logo_url": "https://image.com/"},
        {"name": "롯데 자이언츠", "logo_url": "https://image.com/"},
        {"name": "한화 이글스", "logo_url": "https://image.com/"},
        {"name": "NC 다이노스", "logo_url": "https://image.com/"},
        {"name": "키움 히어로즈", "logo_url": "https://image.com/"},
    ]

    for team_data in teams:
        Team.objects.get_or_create(name=team_data["name"], defaults={"logo_url": team_data["logo_url"]})


def make_user_team_relation():
    user1 = User.objects.get(email="user1@kboapp.com")
    user2 = User.objects.get(email="user2@kboapp.com")
    user3 = User.objects.get(email="user3@kboapp.com")

    team1 = Team.objects.get(name="KIA 타이거즈")
    team2 = Team.objects.get(name="삼성 라이온즈")
    team3 = Team.objects.get(name="LG 트윈스")

    UserTeam.objects.get_or_create(user=user1, team=team1)
    UserTeam.objects.get_or_create(user=user2, team=team2)
    UserTeam.objects.get_or_create(user=user3, team=team3)


def make_friendship():
    user1 = User.objects.get(email="user1@kboapp.com")
    user2 = User.objects.get(email="user2@kboapp.com")
    user3 = User.objects.get(email="user3@kboapp.com")

    Friendship.objects.get_or_create(
        source=user1,
        target=user2,
    )

    Friendship.objects.get_or_create(
        source=user1,
        target=user3,
    )
    Friendship.objects.get_or_create(
        source=user2,
        target=user3,
    )


def run():
    make_auth()
    print("make auth executed.")
    make_users()
    print("make users executed.")
    make_teams()
    print("make teams executed.")
    make_user_team_relation()
    print("make users and teams relation executed.")
    make_friendship()
    print("make friendship executed.")
