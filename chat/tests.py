from django.test import TestCase
from django.contrib.auth.models import User


class ChatTest(TestCase):

    def test_status_code(self):
        user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = user
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get("/chat/room/")
        self.assertEqual(resp.status_code, 200)
