# chat/urls.py
from django.urls import path
from .views import ConversationListCreateView, MessageListCreateView, AllConversationListView

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
    path('all-conversations/', AllConversationListView.as_view(), name='conversation-all'),
    path('conversations/<int:conversation_id>', MessageListCreateView.as_view(), name='message-list'),
]