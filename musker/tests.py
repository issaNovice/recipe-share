from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Meep, Profile

class IntegrationTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='testuser1', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password')
        self.client = Client()
        
        # Log in the first user
        self.client.login(username='testuser1', password='password')

    def test_user_profile_creation(self):
        # Ensure profile is created
        profile = Profile.objects.get(user=self.user1)
        self.assertTrue(profile)
        self.assertIn(profile, profile.follows.all())

    def test_create_meep_and_like(self):
        # Create a Meep
        meep = Meep.objects.create(user=self.user1, body="Integration test meep")
        
        # Ensure the Meep is created correctly
        self.assertEqual(Meep.objects.count(), 1)
        self.assertEqual(meep.body, "Integration test meep")
        self.assertEqual(meep.user, self.user1)
        
        # Log in the second user
        self.client.login(username='testuser2', password='password')

        # Like the Meep
        meep.likes.add(self.user2)

        # Ensure the Meep is liked
        self.assertEqual(meep.number_of_likes(), 1)
        self.assertIn(self.user2, meep.likes.all())

    def test_end_to_end_user_scenario(self):
        # Create a second Meep by the first user
        meep = Meep.objects.create(user=self.user1, body="End-to-end test meep")
        
        # Check initial conditions
        self.assertEqual(Meep.objects.count(), 1)
        self.assertEqual(meep.number_of_likes(), 0)

        # Like the Meep with the second user
        self.client.login(username='testuser2', password='password')
        meep.likes.add(self.user2)
        
        # Ensure the Meep is liked
        self.assertEqual(meep.number_of_likes(), 1)
        self.assertIn(self.user2, meep.likes.all())

        # Verify the string representation
        self.assertEqual(str(meep), f"{self.user1.username} ({meep.created_at:%Y-%m-%d %H:%M}): End-to-end test meep...")

    def tearDown(self):
        User.objects.all().delete()
        Meep.objects.all().delete()
        Profile.objects.all().delete()

if __name__ == '__main__':
    TestCase.main()
