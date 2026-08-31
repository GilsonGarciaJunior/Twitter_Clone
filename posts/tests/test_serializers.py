from django.contrib.auth.models import User
from django.test import TestCase

from posts.models import Post, Like, Comment
from posts.serializers import (
    PostSerializer,
    CommentSerializer,
)


class PostSerializerTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

        self.post = Post.objects.create(
            author=self.user1,
            content='Meu post'
        )

    def test_post_serializer(self):
        serializer = PostSerializer(
            self.post
        )

        self.assertEqual(
            serializer.data['author'],
            'junior'
        )

        self.assertEqual(
            serializer.data['content'],
            'Meu post'
        )

        self.assertEqual(
            serializer.data['likes_count'],
            0
        )

        self.assertFalse(
            serializer.data['liked_by_me']
        )

        self.assertFalse(
            serializer.data['is_owner']
        )

    def test_post_serializer_owner(self):
        request = self.client.get('/')

        request.user = self.user1

        serializer = PostSerializer(
            self.post,
            context={
                'request': request
            }
        )

        self.assertTrue(
            serializer.data['is_owner']
        )

    def test_post_serializer_liked_by_me(self):
        Like.objects.create(
            user=self.user2,
            post=self.post
        )

        request = self.client.get('/')

        request.user = self.user2

        serializer = PostSerializer(
            self.post,
            context={
                'request': request
            }
        )

        self.assertTrue(
            serializer.data['liked_by_me']
        )

        self.assertEqual(
            serializer.data['likes_count'],
            1
        )


class CommentSerializerTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.user2 = User.objects.create_user(
            username='maria',
            password='123456'
        )

        self.post = Post.objects.create(
            author=self.user1,
            content='Meu post'
        )

        self.comment = Comment.objects.create(
            user=self.user1,
            post=self.post,
            content='Meu comentário'
        )

    def test_comment_serializer(self):
        serializer = CommentSerializer(
            self.comment
        )

        self.assertEqual(
            serializer.data['user'],
            'junior'
        )

        self.assertEqual(
            serializer.data['content'],
            'Meu comentário'
        )

        self.assertFalse(
            serializer.data['is_owner']
        )

    def test_comment_serializer_owner(self):
        request = self.client.get('/')

        request.user = self.user1

        serializer = CommentSerializer(
            self.comment,
            context={
                'request': request
            }
        )

        self.assertTrue(
            serializer.data['is_owner']
        )