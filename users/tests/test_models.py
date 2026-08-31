from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from users.models import Profile, Follow


class ProfileModelTest(TestCase):

    def test_profile_is_created(self):
        user = User.objects.create_user(
            username='junior',
            password='123456'
        )

        profile = Profile.objects.create(
            user=user,
            bio='Minha bio'
        )

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.bio, 'Minha bio')
        self.assertEqual(str(profile), 'junior')


class FollowModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

    def test_follow_is_created(self):
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        self.assertEqual(
            follow.follower,
            self.user1
        )

        self.assertEqual(
            follow.following,
            self.user2
        )

        self.assertEqual(
            str(follow),
            'junior segue maria'
        )

    def test_cannot_follow_same_user_twice(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                follower=self.user1,
                following=self.user2
            )