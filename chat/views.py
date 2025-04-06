# chat/views.py
from rest_framework import generics, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, AllConversationSerializer
from django.shortcuts import get_object_or_404
# from django.models.db import Q

# Create your views here.
class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related('participants')
    
    def perform_create(self, serializer):
        participants = serializer.validated_data.get('participants',[])
        participants.append(self.request.user)

        # Create conversation and set participants
        conversation = serializer.save()
        conversation.participants.set(participants)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=self.request.user),
            id=self.kwargs['conversation_id']
        )
        return Message.objects.filter(
            conversation=conversation
        ).select_related('sender').order_by('-created_at')

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=self.request.user),
            id=self.kwargs['conversation_id']
        )
        serializer.save(conversation=conversation, sender=self.request.user)

class AllConversationListView(generics.ListAPIView):
    serializer_class = AllConversationSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        return Conversation.objects.all()