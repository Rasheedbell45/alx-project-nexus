from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Poll, Option, Vote
from rest_framework import status

User = get_user_model()

class PollsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password')
        self.user2 = User.objects.create_user(username='bob', password='password')
        self.client.login   # we will use JWT below or force_authenticate in requests

    def authenticate(self, user):
        # obtain token
        res = self.client.post('/api/users/login/', {'username': user.username, 'password': 'password'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_poll_and_vote_and_results(self):
        # create poll
        self.authenticate(self.user)
        payload = {
            "question": "What's your favorite color?",
            "options": [{"text":"Red"}, {"text":"Blue"}]
        }
        res = self.client.post('/api/polls/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        poll_id = res.data['id']

        # vote as another user
        self.authenticate(self.user2)
        # fetch poll options
        res = self.client.get(f'/api/polls/{poll_id}/', format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        options = res.data['options']
        option_id = options[0]['id']

        # cast vote
        res = self.client.post(f'/api/polls/{poll_id}/vote/', {"option_id": option_id}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # attempt duplicate vote
        res = self.client.post(f'/api/polls/{poll_id}/vote/', {"option_id": option_id}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # results
        res = self.client.get(f'/api/polls/{poll_id}/results/', format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        options = res.data['options']
        # one option should have votes_count 1 (serializer uses votes.count)
        counts = [o['votes_count'] for o in options]
        self.assertIn(1, counts)
