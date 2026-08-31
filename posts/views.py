from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import EmptySerializer

from .models import Post, Like, Comment
from .serializers import (
    PostSerializer,
    CommentSerializer,
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')

        author_id = self.request.query_params.get('author')

        if author_id:
            queryset = queryset.filter(
                author_id=author_id
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    def perform_update(self, serializer):
        post = self.get_object()

        if post.author != self.request.user:
            raise PermissionDenied(
                'Você só pode editar suas próprias postagens.'
            )

        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Você só pode excluir suas próprias postagens.'
            )

        instance.delete()

    @action(
        detail=False,
        methods=['get'],
        url_path='my-posts'
    )
    def my_posts(self, request):
        posts = Post.objects.filter(
            author=request.user
        ).order_by(
            '-created_at'
        )

        serializer = self.get_serializer(
            posts,
            many=True,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='like',
        serializer_class=EmptySerializer,
    )
    def like(self, request, pk=None):
        post = self.get_object()

        if request.method == 'POST':
            like, created = Like.objects.get_or_create(
                user=request.user,
                post=post
            )

            if not created:
                return Response(
                    {
                        'detail':
                        'Você já curtiu esta postagem.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'detail':
                    'Postagem curtida com sucesso.'
                },
                status=status.HTTP_201_CREATED
            )

        deleted, _ = Like.objects.filter(
            user=request.user,
            post=post
        ).delete()

        if deleted == 0:
            return Response(
                {
                    'detail':
                    'Você não curtiu esta postagem.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by(
        '-created_at'
    )

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all().order_by(
            '-created_at'
        )

        post_id = self.request.query_params.get(
            'post'
        )

        if post_id:
            queryset = queryset.filter(
                post_id=post_id
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):
        comment = self.get_object()

        if comment.user != self.request.user:
            raise PermissionDenied(
                'Você só pode editar seus próprios comentários.'
            )

        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(
                'Você só pode excluir seus próprios comentários.'
            )

        instance.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    following_ids = request.user.following.values_list(
        'following_id',
        flat=True
    )

    posts = Post.objects.filter(
        author_id__in=following_ids
    ).select_related(
        'author'
    ).prefetch_related(
        'likes',
        'comments'
    ).order_by(
        '-created_at'
    )

    serializer = PostSerializer(
        posts,
        many=True,
        context={
            'request': request
        }
    )

    return Response(
        serializer.data
    )