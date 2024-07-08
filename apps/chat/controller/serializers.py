# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

from chat.entity.models import ChatRoom, Conversation, GroupMembership, Message, DirectMessaging


User = get_user_model()


class RoomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class GroupMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMembership
        fields = '__all__'


class GroupMessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.StringRelatedField(source = 'conversation')
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'
        

class ChatRoomListSerializer(serializers.ModelSerializer):

    is_full = serializers.BooleanField(read_only=True)
    latest_message = GroupMessageSerializer(source='messages.latest', read_only=True)

    class Meta:
        model = ChatRoom
        exclude = ['members']

class ChatRoomDetailSerializer(serializers.ModelSerializer):
    members = RoomUserSerializer(many=True, read_only = True)
    group_messages = serializers.SerializerMethodField(method_name='get_group_messages')

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'members', 'max_members','avatar', 'date_created', 'group_messages']

    def get_group_messages(self, obj):
        # Retrieve the latest 30 messages for the chat room
        latest_messages = obj.messages.order_by('-timestamp')[:30][::-1]
        
        # Serialize the messages using the GroupMessageSerializer
        serializer = GroupMessageSerializer(latest_messages, many=True)
        
        return serializer.data

class NestedConversationMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    slug_name = serializers.ReadOnlyField()
    last_message = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        # Assuming 'messages' is a related name for Message model in Conversation
        last_message = obj.messages.order_by('-created_at').first()
        if last_message:
            return last_message.content
        return None

    def get_display(self, obj):
        
        user = self.context['request'].user

        display = { 'display_name': obj.name,
                   'avatar': None}
        
        if isinstance(obj, ChatRoom):
            display['avatar'] = obj.avatar.url if obj.avatar else None
        
        elif isinstance(obj, DirectMessaging):
            dm_person = (obj.members.exclude(id=user.id)).first()
            display ['display_name'] = dm_person.name if dm_person else 'Unknown',
            display ['avatar'] = dm_person.avatar.url if dm_person and dm_person.avatar else None
        
        return display

    class Meta:
        model = Conversation
        fields = '__all__'


class DirectMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'

