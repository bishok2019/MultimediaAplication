# chat/serializers.py
from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from account.serializers import UserSerializer

User = get_user_model()

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True)
    participants_detail = UserSerializer(many=True, read_only=True, source='participants')

    class Meta:
        model = Conversation
        fields = ('id', 'participants','participants_detail','created_at', 'updated_at')
        read_only_fields = ('id', 'messages', 'created_at', 'updated_at')

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'conversation', 'sender', 'content', 'read', 'created_at', 'updated_at')
        read_only_fields = ('id', 'sender', 'read', 'created_at', 'updated_at')

class AllConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'participants', 'messages', 'created_at', 'updated_at')
        read_only_fields = ('id', 'participants', 'messages', 'created_at', 'updated_at')