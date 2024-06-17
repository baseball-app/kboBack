from django.test import TestCase, Client
from django.contrib.auth import authenticate, get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse


from users.models import User, Team

User = get_user_model()

class ChangePasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='oldpassword',
            nickname='Test User'
        )
        self.url = reverse('users:change_password', args=[self.user.id])

    def test_change_password_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'current_password': 'oldpassword',
            'new_password': 'newpassword'
        }
        response = self.client.patch(self.url, data, format='json')
        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Password updated successfully'})

        # 비밀번호가 변경되었는지 확인
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

class UpdateMyTeamApiTestCase(APITestCase):
    def setUp(self):
        # 테스트에 필요한 데이터 생성
        self.user = User.objects.create_user(
            email='test@example.com',
            nickname='TestUser',
            password='testpassword'
        )
        self.team = Team.objects.create(
            name='한화이글스',
            logo='test_logo.png'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_my_team_success(self):
        url = reverse('users:update_myteam', args=[self.user.id])
        data = {'team_id': self.team.id}
        response = self.client.patch(url, data, format='json')

        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Team updated successfully'})

        # 사용자의 팀 정보가 업데이트되었는지 확인
        self.user.refresh_from_db()
        self.assertEqual(self.user.my_team, self.team)


