import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify

User = get_user_model()

class AuditableModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Conversation(AuditableModel):
    name = models.CharField(max_length=255, unique=True)

    def is_full(self):
        return self.members.count() >= self.max_members
    
    def user_in_room(self, member_id):
        return self.members.filter(id=member_id).exists()
    
    def user_is_valid_in(self, member_id):
        if self.is_full():
            return False, 'Room is already full.'
        if self.user_in_room(member_id):
            return False, 'User is already a member of this chatroom.'
        return True, 'Valid'
    
    @property
    def slug_name(self):
        return slugify(self.name)

    def __str__(self):
        return self.slug_name
        

class ChatRoom(Conversation):
    members = models.ManyToManyField(User, through='GroupMembership', related_name='my_groups')
    max_members = models.PositiveIntegerField(default=10)
    avatar = models.FileField(upload_to='rooms/avatars/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

class GroupMembership(AuditableModel):
    class UserPermChoice(models.TextChoices):
        REGULAR = 'regular', 'Regular'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    user_perm = models.CharField(
        max_length=50,
        choices=UserPermChoice.choices,
        default=UserPermChoice.REGULAR
    )
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='memberships')
    invite_reason = models.CharField(max_length=64, null=True, blank=True)
    user_title = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        unique_together = ('room', 'member')

    def save(self, *args, **kwargs):
        if self._state.adding:
            is_valid, err_msg = self.room.user_is_valid_in(self.member.id)
            if not is_valid:
                raise ValidationError(err_msg)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_perm}, {self.member} in {self.room.name}"


class Message(AuditableModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to='message/attachments/', null=True, blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True)
    reply_to_tag = models.FileField(upload_to='message/reply_tags/', null=True, blank=True)

    def __str__(self):
        return f"{self.content[:25] or (self.attachment and self.attachment.name)} by {self.sender}"
    
    class Meta:
        ordering = ['-created_at']
        


class DirectMessage(Message):
    conversation = models.ForeignKey('DirectMessaging', on_delete=models.CASCADE, related_name='messages')
    recipient = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'received_direct_messages')

    class Meta:
        ordering = ['-timestamp']

class GroupMessage(Message):
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE, related_name='messages')

    class Meta:
        ordering = ['-timestamp']
        
        get_latest_by = 'timestamp'
