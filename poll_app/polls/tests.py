from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Poll, Option, Vote
from rest_framework_simplejwt.tokens import RefreshToken

class PollsAPITest(APITestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")

        # Auth clients
        self.client1 = APIClient()
        self.client1.login(username="user1", password="pass1234")

        self.client2 = APIClient()
        self.client2.login(username="user2", password="pass1234")

        # Create a poll by user1
        self.poll = Poll.objects.create(question="What is your favorite color?", created_by=self.user1)
        self.option1 = Option.objects.create(poll=self.poll, text="Red")
        self.option2 = Option.objects.create(poll=self.poll, text="Blue")

    def test_list_polls(self):
        response = self.client.get("/polls/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("question", response.data[0])

    def test_create_poll(self):
        data = {"question": "Best programming language?"}
        response = self.client1.post("/polls/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 2)

    def test_poll_detail(self):
        response = self.client.get(f"/polls/{self.poll.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["question"], "What is your favorite color?")

    def test_add_option(self):
        data = {"text": "Green"}
        response = self.client1.post(f"/polls/{self.poll.id}/options/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.poll.options.count(), 3)

    def test_cast_vote(self):
        data = {}
        response = self.client2.post(f"/polls/options/{self.option1.id}/vote/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

    def test_prevent_double_vote(self):
        # First vote should succeed
        self.client2.post(f"/polls/options/{self.option1.id}/vote/")
        # Second vote should fail
        response = self.client2.post(f"/polls/options/{self.option1.id}/vote/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Vote.objects.count(), 1)
    def test_poll_results(self):
        # User2 votes
        self.client2.post(f"/polls/options/{self.option1.id}/vote/")
        # Fetch poll results
        response = self.client.get(f"/polls/{self.poll.id}/results/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        options = response.data["options"]
        votes_count = [opt["votes_count"] for opt in options]
        self.assertIn(1, votes_count)

    def authenticate(self, client, user):
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
