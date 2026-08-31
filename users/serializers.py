from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile, Follow


class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField() 
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_following',
            'is_owner',
            'followers_count', 
            'following_count',
        ]
    def get_is_following(self, obj):
        request = self.context.get('request')

        if not request:
            return False

        if not request.user.is_authenticated:
            return False

        if obj == request.user:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj == request.user
    
    def get_followers_count(self, obj): 
        return Follow.objects.filter( 
            following=obj 
        ).count() 
    
    def get_following_count(self, obj): 
        return Follow.objects.filter( 
            follower=obj 
        ).count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    password_confirm = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_confirm',
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {
                    'password_confirm':
                    'As senhas não coincidem.'
                }
            )

        return data

    def validate_username(self, value):
        if User.objects.filter(
            username=value
        ).exists():
            raise serializers.ValidationError(
                'Este username já está em uso.'
            )

        return value

    def create(self, validated_data):
        validated_data.pop(
            'password_confirm'
        )

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get(
                'email',
                ''
            ),
            password=validated_data['password'],
            first_name=validated_data.get(
                'first_name',
                ''
            ),
            last_name=validated_data.get(
                'last_name',
                ''
            )
        )

        Profile.objects.create(
            user=user
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                'Nome de usuário ou senha inválidos.'
            )

        data['user'] = user

        return data


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    first_name = serializers.CharField(
        source='user.first_name',
        required=False
    )

    last_name = serializers.CharField(
        source='user.last_name',
        required=False
    )

    email = serializers.EmailField(
        source='user.email',
        required=False
    )

    class Meta:
        model = Profile

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'foto',
            'bio',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop(
            'user',
            {}
        )

        user = instance.user

        user.first_name = user_data.get(
            'first_name',
            user.first_name
        )

        user.last_name = user_data.get(
            'last_name',
            user.last_name
        )

        user.email = user_data.get(
            'email',
            user.email
        )

        user.save()

        instance.foto = validated_data.get(
            'foto',
            instance.foto
        )

        instance.bio = validated_data.get(
            'bio',
            instance.bio
        )

        instance.save()

        return instance

class EmptySerializer(serializers.Serializer):
    pass