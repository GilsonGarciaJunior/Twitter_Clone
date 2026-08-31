from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    PostViewSet,
    feed,
)

router = DefaultRouter()

router.register(
    'posts',
    PostViewSet,
    basename='posts'
)

router.register(
    'comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path(
        'feed/',
        feed,
        name='feed'
    ),
]

urlpatterns += router.urls