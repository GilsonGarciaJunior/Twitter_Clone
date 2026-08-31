from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import Follow
from .serializers import (
    EmptySerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterViewSet(ViewSet):
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        return RegisterSerializer(
            *args,
            **kwargs
        )

    def create(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                'message':
                'Usuário criado com sucesso.',
                'user':
                UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )


class AuthViewSet(ViewSet):
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(
            *args,
            **kwargs
        )

    @action(
        detail=False,
        methods=['post']
    )
    def login(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data['user']

        login(
            request,
            user
        )

        return Response(
            {
                'message':
                'Login realizado com sucesso.',
                'user':
                UserSerializer(user).data,
            }
        )

    @action(
        detail=False,
        methods=['post']
    )
    def logout(self, request):
        if not request.user.is_authenticated:
            return Response(
                {
                    'detail':
                    'Você não está autenticado.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        logout(request)

        return Response(
            {
                'message':
                'Logout realizado com sucesso.'
            }
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='follow',
        serializer_class=EmptySerializer,
    )
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(
                {
                    'detail':
                    'Você não pode seguir a si mesmo.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            follow, created = Follow.objects.get_or_create(
                follower=request.user,
                following=user_to_follow
            )

            if not created:
                return Response(
                    {
                        'detail':
                        'Você já segue este usuário.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'message':
                    f'Agora você segue '
                    f'{user_to_follow.username}.'
                },
                status=status.HTTP_201_CREATED
            )

        deleted, _ = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        ).delete()

        if deleted == 0:
            return Response(
                {
                    'detail':
                    'Você não segue este usuário.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'message':
                f'Você deixou de seguir '
                f'{user_to_follow.username}.'
            }
        )

    @action(
        detail=True,
        methods=['get'],
        url_path='profile'
    )
    def profile(self, request, pk=None):
        user = self.get_object()

        serializer = UserSerializer(
            user,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )

class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(
            *args,
            **kwargs
        )

    def retrieve(self, request):
        profile = request.user.profile

        serializer = self.get_serializer(
            profile,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )

    def partial_update(self, request):
        profile = request.user.profile

        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True,
            context={
                'request': request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data
        )


class FollowersViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        followers = User.objects.filter(
            following__following=request.user
        ).distinct()

        serializer = UserSerializer(
            followers,
            many=True,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )


class FollowingViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        following = User.objects.filter(
            followers__follower=request.user
        ).distinct()

        serializer = UserSerializer(
            following,
            many=True,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )

def public_profile(request, user_id):
    return render(
        request,
        'perfil_publico.html',
        {
            'user_id': user_id
        }
    )