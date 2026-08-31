from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthViewSet,
    FollowersViewSet,
    FollowingViewSet,
    ProfileViewSet,
    RegisterViewSet,
    UserViewSet,
    public_profile,
)


router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

router.register(
    'auth/register',
    RegisterViewSet,
    basename='register'
)


urlpatterns = [
    path(
        'auth/login/',
        AuthViewSet.as_view({
            'post': 'login'
        }),
        name='login'
    ),

    path(
        'auth/logout/',
        AuthViewSet.as_view({
            'post': 'logout'
        }),
        name='logout'
    ),

    path(
        'profile/',
        ProfileViewSet.as_view({
            'get': 'retrieve',
        }),
        name='profile'
    ),

    path(
        'profile/update/',
        ProfileViewSet.as_view({
            'patch': 'partial_update',
        }),
        name='profile-update'
    ),

    path(
        'followers/',
        FollowersViewSet.as_view({
            'get': 'list'
        }),
        name='followers'
    ),

    path(
        'following/',
        FollowingViewSet.as_view({
            'get': 'list'
        }),
        name='following'
    ),
    
]

urlpatterns += router.urls