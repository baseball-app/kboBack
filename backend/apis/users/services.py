from django.contrib.auth import get_user_model

from apps.users.models import Friendship

User = get_user_model()


class UserFollowService:
    def make_relation(self, source_id, target_id):
        s_user = User.objects.get(id=source_id)
        t_user = User.objects.get(id=target_id)
        Friendship.objects.create(source=s_user, target=t_user)

    def release_relation(self, source_id, target_id):
        s_user = User.objects.get(id=source_id)
        t_user = User.objects.get(id=target_id)
        Friendship.objects.filter(source=s_user, target=t_user).delete()
        Friendship.objects.filter(source=t_user, target=s_user).delete()
