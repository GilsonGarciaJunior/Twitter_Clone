from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from posts.models import Post, Like, Comment


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='junior',
            password='123456'
        )

    def test_post_is_created(self):
        post = Post.objects.create(
            author=self.user,
            content='Meu primeiro post'
        )

        self.assertEqual(
            post.author,
            self.user
        )

        self.assertEqual(
            post.content,
            'Meu primeiro post'
        )

        self.assertEqual(
            str(post),
            'junior: Meu primeiro post'
        )


class LikeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.post = Post.objects.create(
            author=self.user,
            content='Meu post'
        )

    def test_like_is_created(self):
        like = Like.objects.create(
            user=self.user,
            post=self.post
        )

        self.assertEqual(
            like.user,
            self.user
        )

        self.assertEqual(
            like.post,
            self.post
        )

        self.assertEqual(
            str(like),
            f'junior curtiu o post {self.post.id}'
        )

    def test_cannot_like_same_post_twice(self):
        Like.objects.create(
            user=self.user,
            post=self.post
        )

        with self.assertRaises(IntegrityError):
            Like.objects.create(
                user=self.user,
                post=self.post
            )


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='junior',
            password='123456'
        )

        self.post = Post.objects.create(
            author=self.user,
            content='Meu post'
        )

    def test_comment_is_created(self):
        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Ótimo post!'
        )

        self.assertEqual(
            comment.user,
            self.user
        )

        self.assertEqual(
            comment.post,
            self.post
        )

        self.assertEqual(
            comment.content,
            'Ótimo post!'
        )

        self.assertEqual(
            str(comment),
            'junior: Ótimo post!'
        )

    def test_delete_post_deletes_comments_and_likes(self):
        like = Like.objects.create(
            user=self.user,
            post=self.post
        )

        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Comentário'
        )

        self.post.delete()

        self.assertFalse(
            Like.objects.filter(
                id=like.id
            ).exists()
        )

        self.assertFalse(
            Comment.objects.filter(
                id=comment.id
            ).exists()
        )