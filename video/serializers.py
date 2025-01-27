from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    # Custom field to get the author's email
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'updated_at','author_email','file','likes', 'dislikes']
        read_only_fields = ['likes', 'dislikes']