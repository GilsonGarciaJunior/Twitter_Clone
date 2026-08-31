from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from posts.models import Post, Like, Comment
from posts.views import (
    PostViewSet,
    CommentViewSet,
    feed,
)


class PostViewSetTest(TestCase):

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

        self.post = Post.objects.create(
            author=self.user1,
            content='Post do Junior'
        )

        self.post2 = Post.objects.create(
            author=self.user2,
            content='Post da Maria'
        )

    def test_create_post(self):
        request = self.factory.post(
            '/posts/',
            {
                'content': 'Novo post'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = PostViewSet.as_view({
            'post': 'create'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            Post.objects.filter(
                author=self.user1,
                content='Novo post'
            ).exists()
        )

def test_create_post_uses_authenticated_user(self):
    request = self.factory.post(
        '/posts/',
        {
            'content': 'Post criado pela Maria'
        },
        format='json'
    )

    force_authenticate(
        request,
        user=self.user2
    )

    view = PostViewSet.as_view({
        'post': 'create'
    })

    response = view(request)

    self.assertEqual(
        response.status_code,
        201
    )

    post = Post.objects.get(
        content='Post criado pela Maria'
    )

    self.assertEqual(
        post.author,
        self.user2
    )



    def test_update_own_post(self):
        request = self.factory.patch(
            f'/posts/{self.post.id}/',
            {
                'content': 'Post editado'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = PostViewSet.as_view({
            'patch': 'partial_update'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.post.refresh_from_db()

        self.assertEqual(
            self.post.content,
            'Post editado'
        )

    def test_cannot_update_other_user_post(self):
        request = self.factory.patch(
            f'/posts/{self.post.id}/',
            {
                'content': 'Tentativa de edição'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = PostViewSet.as_view({
            'patch': 'partial_update'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            403
        )

        self.post.refresh_from_db()

        self.assertEqual(
            self.post.content,
            'Post do Junior'
        )

    def test_delete_own_post(self):
        request = self.factory.delete(
            f'/posts/{self.post.id}/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = PostViewSet.as_view({
            'delete': 'destroy'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            204
        )

        self.assertFalse(
            Post.objects.filter(
                id=self.post.id
            ).exists()
        )

    def test_cannot_delete_other_user_post(self):
        request = self.factory.delete(
            f'/posts/{self.post.id}/'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = PostViewSet.as_view({
            'delete': 'destroy'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            403
        )

        self.assertTrue(
            Post.objects.filter(
                id=self.post.id
            ).exists()
        )

    def test_like_post(self):
        request = self.factory.post(
            f'/posts/{self.post.id}/like/'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = PostViewSet.as_view({
            'post': 'like'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            Like.objects.filter(
                user=self.user2,
                post=self.post
            ).exists()
        )

    def test_cannot_like_same_post_twice(self):
        Like.objects.create(
            user=self.user2,
            post=self.post
        )

        request = self.factory.post(
            f'/posts/{self.post.id}/like/'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = PostViewSet.as_view({
            'post': 'like'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_unlike_post(self):
        Like.objects.create(
            user=self.user2,
            post=self.post
        )

        request = self.factory.delete(
            f'/posts/{self.post.id}/like/'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = PostViewSet.as_view({
            'delete': 'like'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            204
        )

        self.assertFalse(
            Like.objects.filter(
                user=self.user2,
                post=self.post
            ).exists()
        )

    def test_unlike_when_not_liked(self):
        request = self.factory.delete(
            f'/posts/{self.post.id}/like/'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = PostViewSet.as_view({
            'delete': 'like'
        })

        response = view(
            request,
            pk=self.post.id
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_my_posts(self):
        Post.objects.create(
            author=self.user1,
            content='Segundo post'
        )

        request = self.factory.get(
            '/posts/my-posts/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = PostViewSet.as_view({
            'get': 'my_posts'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            1 + 1
        )

        for post in response.data:
            self.assertEqual(
                post['author'],
                'junior'
            )


class CommentViewSetTest(TestCase):

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

        self.post = Post.objects.create(
            author=self.user1,
            content='Meu post'
        )

        self.comment = Comment.objects.create(
            user=self.user1,
            post=self.post,
            content='Comentário original'
        )

    def test_create_comment(self):
        request = self.factory.post(
            '/comments/',
            {
                'post': self.post.id,
                'content': 'Novo comentário'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = CommentViewSet.as_view({
            'post': 'create'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            Comment.objects.filter(
                user=self.user2,
                post=self.post,
                content='Novo comentário'
            ).exists()
        )

    def test_list_comments_by_post(self):
        Comment.objects.create(
            user=self.user2,
            post=self.post,
            content='Outro comentário'
        )

        request = self.factory.get(
            f'/comments/?post={self.post.id}'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = CommentViewSet.as_view({
            'get': 'list'
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            2
        )

    def test_update_own_comment(self):
        request = self.factory.patch(
            f'/comments/{self.comment.id}/',
            {
                'content': 'Comentário editado'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = CommentViewSet.as_view({
            'patch': 'partial_update'
        })

        response = view(
            request,
            pk=self.comment.id
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.comment.refresh_from_db()

        self.assertEqual(
            self.comment.content,
            'Comentário editado'
        )

    def test_cannot_update_other_user_comment(self):
        request = self.factory.patch(
            f'/comments/{self.comment.id}/',
            {
                'content': 'Tentativa'
            },
            format='json'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = CommentViewSet.as_view({
            'patch': 'partial_update'
        })

        response = view(
            request,
            pk=self.comment.id
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_delete_own_comment(self):
        request = self.factory.delete(
            f'/comments/{self.comment.id}/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        view = CommentViewSet.as_view({
            'delete': 'destroy'
        })

        response = view(
            request,
            pk=self.comment.id
        )

        self.assertEqual(
            response.status_code,
            204
        )

        self.assertFalse(
            Comment.objects.filter(
                id=self.comment.id
            ).exists()
        )

    def test_cannot_delete_other_user_comment(self):
        request = self.factory.delete(
            f'/comments/{self.comment.id}/'
        )

        force_authenticate(
            request,
            user=self.user2
        )

        view = CommentViewSet.as_view({
            'delete': 'destroy'
        })

        response = view(
            request,
            pk=self.comment.id
        )

        self.assertEqual(
            response.status_code,
            403
        )


class FeedViewTest(TestCase):

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

        self.post_followed = Post.objects.create(
            author=self.user2,
            content='Post da Maria'
        )

        self.post_not_followed = Post.objects.create(
            author=self.user3,
            content='Post do João'
        )

    def test_feed_only_shows_followed_users(self):
        from users.models import Follow

        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        request = self.factory.get(
            '/feed/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        response = feed(request)

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]['author'],
            'maria'
        )

        self.assertEqual(
            response.data[0]['content'],
            'Post da Maria'
        )

    def test_feed_is_empty_without_following(self):
        request = self.factory.get(
            '/feed/'
        )

        force_authenticate(
            request,
            user=self.user1
        )

        response = feed(request)

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            0
        )