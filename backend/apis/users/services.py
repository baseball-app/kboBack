import base64
import uuid

from django.contrib.auth import get_user_model

from apps.users.models import Friendship

User = get_user_model()


class UserFollowService:
    def make_relation(self, source_id, target_id):
        s_user = User.objects.get(id=source_id)
        t_user = User.objects.get(id=target_id)
        Friendship.objects.create(source=s_user, target=t_user)
        Friendship.objects.create(source=t_user, target=s_user)

    def release_relation(self, source_id, target_id):
        s_user = User.objects.get(id=source_id)
        t_user = User.objects.get(id=target_id)
        Friendship.objects.filter(source=s_user, target=t_user).delete()
        Friendship.objects.filter(source=t_user, target=s_user).delete()


class UserInvitationService:
    def generate_invite_code(self, user_id):
        unique_id = uuid.uuid4()
        raw_code = f'{unique_id}:{user_id}'
        encoded_code = base64.urlsafe_b64encode(raw_code.encode()).decode()
        return encoded_code

    def decode_invite_code(self, invite_code):
        decoded_code = base64.urlsafe_b64decode(invite_code).decode()
        unique_id, user_id = decoded_code.split(':')
        return user_id
