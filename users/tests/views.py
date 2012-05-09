from django.test import TestCase
from django.test.client import Client
from factories import UserFactory

class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()

    def test_user_detail(self):
        response = self.client.get('/users/%d/' % self.user.pk)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
