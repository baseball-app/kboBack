import base64
import uuid

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q

from apps.auths.models import SocialInfo
from apps.notifications.models import Notification
from apps.teams.models import UserTeam, Team
from apps.tickets.models import Ticket
from apps.users.models import Friendship

User = get_user_model()


class UserFollowService:
    def make_relation(self, source_id, target_id):
        if source_id == target_id:
            return
        s_user = User.objects.get(id=source_id)
        t_user = User.objects.get(id=target_id)
        Friendship.objects.create(source=s_user, target=t_user)
        Friendship.objects.create(source=t_user, target=s_user)

    def release_relation(self, source_id, target_id):
        if source_id == target_id:
            return
        s_user = User.objects.get(id=source_id)
        t_user = User.objects.get(id=target_id)
        Friendship.objects.filter(source=s_user, target=t_user).delete()
        Friendship.objects.filter(source=t_user, target=s_user).delete()


class UserInvitationService:
    def generate_invite_code(self, user_id):
        unique_id = uuid.uuid4()
        raw_code = f"{unique_id}:{user_id}"
        encoded_code = base64.urlsafe_b64encode(raw_code.encode()).decode()
        return encoded_code

    def decode_invite_code(self, invite_code):
        decoded_code = base64.urlsafe_b64decode(invite_code).decode()
        unique_id, user_id = decoded_code.split(":")
        return user_id


class UserLeaveService:
    @transaction.atomic
    def leave(self, user_id):
        user = User.objects.get(id=user_id)
        SocialInfo.objects.filter(user_id=user_id).delete()
        UserTeam.objects.filter(user_id=user_id).delete()
        Friendship.objects.filter(Q(source_id=user_id) | Q(target_id=user_id)).delete()
        Notification.objects.filter(Q(user_id=user_id) | Q(feedback_user=user_id)).delete()
        user.delete()


class UserModifyService:
    def modify(self, user, validated_data):
        update_fields = {k: v for k, v in validated_data.items() if k in ["nickname", "profile_type"] and v}

        if update_fields:
            user.__dict__.update(update_fields)
            user.save(update_fields=update_fields.keys())

        if "my_team" in validated_data and validated_data["my_team"]:
            team = Team.objects.get(id=validated_data["my_team"])
            if not team:
                return

            user_team, created = UserTeam.objects.get_or_create(team=team, user=user)
            if not created:
                user_team.team = team
                user_team.save()
                user = user_team.user

                Ticket.objects.filter(writer=user).delete()
