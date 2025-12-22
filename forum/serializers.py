from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source="author.username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "author_name",
            "text",
            "created_at",
        ]
        read_only_fields = ("author", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source="author.username",
        read_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "created_at",
            "comments",
        ]
        read_only_fields = ("author", "created_at")
