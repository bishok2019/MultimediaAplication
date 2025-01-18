from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # Custom field to get the author's email
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_at', 'updated_at','author_email']