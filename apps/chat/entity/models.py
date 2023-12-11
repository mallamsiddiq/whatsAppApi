from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length = 255)
    members = models.ManyToManyField(User, through = 'GroupMembership', related_name = 'my_groups')
    max_members = models.PositiveIntegerField(default = 10)
    avatar = models.FileField(upload_to = 'rooms/avaters/', null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def is_full(self):
        return self.members.count() >=  self.max_members
    
    def user_in_room(self, member_id):
        return self.members.filter(id = member_id).count() > 0
    
    def user_is_valid_in(self, member_id):

        if self.is_full():
            return False, 'Room is already filled'
        if self.user_in_room(member_id):
            return False, "User is already a member of this chatroom."
        return True, 'valid'

    def __str__(self) -> str:
        return self.name
    
class GroupMembership(models.Model):
    class UserPermChoice(models.TextChoices):
        REGULAR = "regular", "Regular"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Admin"

    user_perm = models.CharField(
        max_length = 50,
        choices = UserPermChoice.choices,
        default = UserPermChoice.REGULAR
    )
    member = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'memberships')
    room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE, related_name = 'memberships')
    date_joined = models.DateTimeField(auto_now_add = True)
    invite_reason = models.CharField(max_length = 64, null = True, blank = True)
    user_title = models.CharField(max_length = 64, null = True, blank = True)

    def save(self, *args, **kwargs):

        is_valid, err_msg = self.room.user_is_valid_in(self.member.id)
        if not is_valid:
            raise ValidationError(err_msg)

        super(GroupMembership, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_perm}, {self.member} in {self.room.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'authored_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to = 'message/attachments/', null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    reply_to = models.ForeignKey('self', on_delete = models.SET_NULL, related_name = 'replies', null = True)

    def __str__(self) -> str:
        return f"{self.content[:25] or (self.attachment and self.attachment.name) } by {self.sender}"

class DirectMessage(Message):
    recipient = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'received_direct_messages')

class GroupMessage(Message):
    chat_room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE, related_name = 'group_messages')