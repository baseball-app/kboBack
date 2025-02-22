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


import csv
from datetime import datetime
from django.utils import timezone
from apps.teams.models import Team
from apps.games.models import Ballpark, Game


def make_ballparks():
    ballpark_data = {
        "잠실": {"name": "잠실야구장", "teams": ["LG 트윈스", "두산 베어스"]},
        "고척": {"name": "고척스카이돔", "teams": ["키움 히어로즈"]},
        "문학": {"name": "인천SSG랜더스필드", "teams": ["SSG 랜더스"]},
        "수원": {"name": "수원 케이티 위즈 파크", "teams": ["KT 위즈"]},
        "대전": {"name": "대전한화생명 이글스파크", "teams": ["한화 이글스"]},
        "대구": {"name": "대구삼성라이온즈파크", "teams": ["삼성 라이온즈"]},
        "광주": {"name": "광주-기아 챔피언스 필드", "teams": ["KIA 타이거즈"]},
        "사직": {"name": "사직야구장", "teams": ["롯데 자이언츠"]},
        "창원": {"name": "창원NC파크", "teams": ["NC 다이노스"]},
    }

    for short_name, data in ballpark_data.items():
        print(short_name, data)
        for team_name in data["teams"]:
            team = Team.objects.get(name=team_name)
            Ballpark.objects.get_or_create(name=data["name"], team=team)
    print("Ballparks created successfully.")


def get_team_from_ballpark(ballpark_short_name):
    ballpark_team_map = {
        "잠실": ["LG 트윈스", "두산 베어스"],
        "고척": ["키움 히어로즈"],
        "문학": ["SSG 랜더스"],
        "수원": ["KT 위즈"],
        "대전": ["한화 이글스"],
        "대구": ["삼성 라이온즈"],
        "광주": ["KIA 타이거즈"],
        "사직": ["롯데 자이언츠"],
        "창원": ["NC 다이노스"],
    }
    return ballpark_team_map.get(ballpark_short_name, [None])[0]


def get_team_name_mapping():
    return {
        "NC": "NC 다이노스",
        "SSG": "SSG 랜더스",
        "KIA": "KIA 타이거즈",
        "KT": "KT 위즈",
        "삼성": "삼성 라이온즈",
        "한화": "한화 이글스",
        "두산": "두산 베어스",
        "롯데": "롯데 자이언츠",
        "LG": "LG 트윈스",
        "키움": "키움 히어로즈",
    }


def parse_team_name(team_name):
    if "-" in team_name:
        team_short_name = team_name.split("-")[1]
    else:
        team_short_name = team_name

    team_mapping = get_team_name_mapping()
    for short_name, full_name in team_mapping.items():
        if team_short_name.startswith(short_name):
            return full_name

    return team_name


def make_games():
    team_mapping = get_team_name_mapping()

    csv_path = "game_info.csv"

    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            game_count = 0
            for row in csv_reader:
                if not row.get("월") or not row.get("일"):
                    continue

                month = int(row["월"])
                day = int(row["일"])

                for ballpark_short_name, match_info in row.items():
                    if ballpark_short_name in ["월", "일", "요일"] or not match_info:
                        continue

                    if "-" in match_info:
                        away_team_short, home_team_short = match_info.split("-")

                        away_team_name = team_mapping.get(away_team_short)
                        home_team_name = team_mapping.get(home_team_short)

                        if not away_team_name or not home_team_name:
                            print(f"Could not map team names: {away_team_short}-{home_team_short}")
                            continue

                        game_date = datetime(2024, month, day)
                        game_date = timezone.make_aware(game_date)

                        try:
                            home_team = Team.objects.get(name=home_team_name)
                            away_team = Team.objects.get(name=away_team_name)

                            ballpark = Ballpark.objects.filter(team=home_team).first()
                            if not ballpark:
                                print(f"No ballpark found for {home_team_name}, trying to find one...")

                                for bp in Ballpark.objects.all():
                                    print(f"Available ballpark: {bp.name} for team {bp.team}")

                                ballparks = Ballpark.objects.filter(name__contains=ballpark_short_name)
                                if ballparks.exists():
                                    ballpark = ballparks.first()
                                    print(f"Found ballpark by name: {ballpark.name}")
                                else:
                                    print(f"Could not find a ballpark for {home_team_name}, skipping game")
                                    continue

                            game, created = Game.objects.get_or_create(
                                team_home=home_team, team_away=away_team, ballpark=ballpark, game_date=game_date
                            )

                            if created:
                                game_count += 1
                                print(f"Created game: {away_team_name} at {home_team_name} on {game_date}")
                            else:
                                print(f"Game already exists: {away_team_name} at {home_team_name} on {game_date}")

                        except (Team.DoesNotExist, Ballpark.DoesNotExist) as e:
                            print(f"Error creating game: {away_team_name} vs {home_team_name}")
                            print(f"Error details: {str(e)}")
                    else:
                        print(f"Invalid match format (no dash): {match_info} at {ballpark_short_name}")

            print(f"Games created successfully: {game_count} new games added.")
    except FileNotFoundError:
        print(f"CSV file not found at path: {csv_path}")
        print("Please make sure your game schedule CSV is uploaded and named correctly.")
    except Exception as e:
        print(f"An error occurred while reading the CSV: {str(e)}")


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
    make_ballparks()
    make_games()
