from django.contrib import admin
from chat.entity.models import GroupMembership, DirectMessage, GroupMessage, Message, ChatRoom


[admin.site.register(obj) for obj in 
 (GroupMembership, DirectMessage, GroupMessage, Message, ChatRoom)]
# Register your models here.
