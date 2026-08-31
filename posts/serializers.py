from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    likes_count = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post

        fields = [
            'id',
            'author',
            'content',
            'likes_count',
            'liked_by_me',
            'is_owner',
            'created_at',
            'updated_at',
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_liked_by_me(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.likes.filter(
            user=request.user
        ).exists()
    
    def get_is_owner(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.author == request.user



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True
    )

    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment

        fields = [
            'id',
            'user',
            'post',
            'content',
            'created_at',
            'is_owner',
        ]

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if not request:
            return False

        if not request.user.is_authenticated:
            return False

        return obj.user == request.user