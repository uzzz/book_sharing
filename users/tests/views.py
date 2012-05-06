from django.test import TestCase
from django.test.client import Client
from factories import UserFactory

class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()

    def testUserDetail(self):
        response = self.client.get('/users/' + str(self.user.pk) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
