#chat/models.py
from django.db import models
from django.conf import settings
from base.models import BaseModel
# Create your models here.
class Conversation(BaseModel):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversation {self.id}"

class Message(BaseModel):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    read = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

        def __str__(self):
            return f"Message from {self.sender.username}"