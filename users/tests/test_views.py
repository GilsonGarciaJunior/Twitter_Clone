from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import Profile, Follow
from users.views import (
    UserViewSet,
    FollowersViewSet,
    FollowingViewSet,
    ProfileViewSet,
)


class UserViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

    def test_follow_user(self):
        request = self.factory.post(
            '/users/2/follow/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = UserViewSet.as_view({
            'post': 'follow'
        })

        response = view(
            request,
            pk=self.user2.id
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )

    def test_cannot_follow_same_user(self):
        request = self.factory.post(
            '/users/1/follow/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = UserViewSet.as_view({
            'post': 'follow'
        })

        response = view(
            request,
            pk=self.user1.id
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_cannot_follow_same_user_twice(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        request = self.factory.post(
            '/users/2/follow/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = UserViewSet.as_view({
            'post': 'follow'
        })

        response = view(
            request,
            pk=self.user2.id
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_unfollow_user(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        request = self.factory.delete(
            '/users/2/follow/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = UserViewSet.as_view({
            'delete': 'follow'
        })

        response = view(
            request,
            pk=self.user2.id
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertFalse(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )

    def test_unfollow_when_not_following(self):
        request = self.factory.delete(
            '/users/2/follow/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = UserViewSet.as_view({
            'delete': 'follow'
        })

        response = view(
            request,
            pk=self.user2.id
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_public_profile_data(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        request = self.factory.get(
            '/users/2/profile/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = UserViewSet.as_view({
            'get': 'profile'
        })

        response = view(
            request,
            pk=self.user2.id
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data['username'],
            'maria'
        )

        self.assertTrue(
            response.data['is_following']
        )

        self.assertFalse(
            response.data['is_owner']
        )


class FollowersViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

        self.user3 = User.objects.create_user(
            username='joao',
            password='123456'
        )

    def test_followers_list(self):
        Follow.objects.create(
            follower=self.user2,
            following=self.user1
        )

        Follow.objects.create(
            follower=self.user3,
            following=self.user1
        )

        request = self.factory.get(
            '/followers/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = FollowersViewSet.as_view({
            'get': 'list'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200
        )

        usernames = [
            user['username']
            for user in response.data
        ]

        self.assertIn(
            'maria',
            usernames
        )

        self.assertIn(
            'joao',
            usernames
        )


class FollowingViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

        self.user3 = User.objects.create_user(
            username='joao',
            password='123456'
        )

    def test_following_list(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        Follow.objects.create(
            follower=self.user1,
            following=self.user3
        )

        request = self.factory.get(
            '/following/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = FollowingViewSet.as_view({
            'get': 'list'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200
        )

        usernames = [
            user['username']
            for user in response.data
        ]

        self.assertIn(
            'maria',
            usernames
        )

        self.assertIn(
            'joao',
            usernames
        )


class ProfileViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username='junior',
            first_name='Junior',
            last_name='Rodrigues',
            email='old@email.com',
            password='123456'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            bio='Bio antiga'
        )

    def test_get_my_profile(self):
        request = self.factory.get(
            '/profile/'
        )

        force_authenticate(
            request,
            user=self.user
        )

        view = ProfileViewSet.as_view({
            'get': 'retrieve'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data['username'],
            'junior'
        )

        self.assertEqual(
            response.data['bio'],
            'Bio antiga'
        )

    def test_update_my_profile(self):
        request = self.factory.patch(
            '/profile/update/',
            {
                'first_name': 'Novo',
                'bio': 'Nova bio'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user
        )

        view = ProfileViewSet.as_view({
            'patch': 'partial_update'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200
        )

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            'Novo'
        )

        self.assertEqual(
            self.profile.bio,
            'Nova bio'
        )