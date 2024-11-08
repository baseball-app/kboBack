import toml
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application

from conf.settings.base import BASE_DIR

User = get_user_model()
config = toml.load(BASE_DIR / "config.toml")


def run():
    email = config["init"]["email"]
    nickname = config["init"]["nickname"]
    password = config["init"]["password"]

    try:
        default_user = User.objects.get(
            email=email
        )
    except User.DoesNotExist:
        default_user = User.objects.create(
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
            name='dev',
            client_id=client_id,
            client_secret=client_secret,
            client_type=client_type,
            authorization_grant_type=authorization_grant_type,
            redirect_uris=redirect_uris,
            user_id=default_user.id,
        )

    print("init script executed.")
