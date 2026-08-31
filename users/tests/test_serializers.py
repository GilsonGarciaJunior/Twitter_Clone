from django.contrib.auth.models import User
from django.test import TestCase

from users.models import Profile, Follow
from users.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
)


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

    def test_user_serializer(self):
        serializer = UserSerializer(
            self.user1
        )

        self.assertEqual(
            serializer.data['username'],
            'junior'
        )

        self.assertEqual(
            serializer.data['is_following'],
            False
        )

        self.assertEqual(
            serializer.data['is_owner'],
            False
        )

    def test_user_serializer_following(self):
        request = self.client.get('/')

        request.user = self.user1

        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        serializer = UserSerializer(
            self.user2,
            context={
                'request': request
            }
        )

        self.assertTrue(
            serializer.data['is_following']
        )

        self.assertTrue(
            serializer.data['following_count'] == 0
        )

        self.assertTrue(
            serializer.data['followers_count'] == 1
        )

    def test_user_serializer_owner(self):
        request = self.client.get('/')

        request.user = self.user1

        serializer = UserSerializer(
            self.user1,
            context={
                'request': request
            }
        )

        self.assertTrue(
            serializer.data['is_owner']
        )


class RegisterSerializerTest(TestCase):

    def test_register_serializer_is_valid(self):
        data = {
            'username': 'junior',
            'first_name': 'Junior',
            'last_name': 'Rodrigues',
            'email': 'junior@email.com',
            'password': '123456',
            'password_confirm': '123456',
        }

        serializer = RegisterSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_register_creates_user_and_profile(self):
        data = {
            'username': 'junior',
            'first_name': 'Junior',
            'last_name': 'Rodrigues',
            'email': 'junior@email.com',
            'password': '123456',
            'password_confirm': '123456',
        }

        serializer = RegisterSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        self.assertTrue(
            User.objects.filter(
                username='junior'
            ).exists()
        )

        self.assertTrue(
            Profile.objects.filter(
                user=user
            ).exists()
        )

        self.assertTrue(
            user.check_password('123456')
        )

    def test_password_confirmation(self):
        data = {
            'username': 'junior',
            'password': '123456',
            'password_confirm': '654321',
        }

        serializer = RegisterSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            'password_confirm',
            serializer.errors
        )

    def test_username_cannot_be_repeated(self):
        User.objects.create_user(
            username='junior',
            password='123456'
        )

        data = {
            'username': 'junior',
            'password': '123456',
            'password_confirm': '123456',
        }

        serializer = RegisterSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            'username',
            serializer.errors
        )


class LoginSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='junior',
            password='123456'
        )

    def test_login_is_valid(self):
        serializer = LoginSerializer(
            data={
                'username': 'junior',
                'password': '123456',
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data['user'],
            self.user
        )

    def test_login_with_wrong_password(self):
        serializer = LoginSerializer(
            data={
                'username': 'junior',
                'password': 'wrong-password',
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )


class ProfileSerializerTest(TestCase):

    def setUp(self):
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

    def test_profile_serializer(self):
        serializer = ProfileSerializer(
            self.profile
        )

        self.assertEqual(
            serializer.data['username'],
            'junior'
        )

        self.assertEqual(
            serializer.data['first_name'],
            'Junior'
        )

        self.assertEqual(
            serializer.data['last_name'],
            'Rodrigues'
        )

        self.assertEqual(
            serializer.data['email'],
            'old@email.com'
        )

        self.assertEqual(
            serializer.data['bio'],
            'Bio antiga'
        )

    def test_profile_update(self):
        serializer = ProfileSerializer(
            self.profile,
            data={
                'first_name': 'Novo',
                'last_name': 'Nome',
                'email': 'new@email.com',
                'bio': 'Nova bio',
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            'Novo'
        )

        self.assertEqual(
            self.user.last_name,
            'Nome'
        )

        self.assertEqual(
            self.user.email,
            'new@email.com'
        )

        self.assertEqual(
            self.profile.bio,
            'Nova bio'
        )