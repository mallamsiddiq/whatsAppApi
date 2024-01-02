# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model


from chat.entity.models import ChatRoom, DirectMessage, GroupMessage, GroupMembership

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
    chat_room = serializers.StringRelatedField()
    sender = serializers.StringRelatedField()

    class Meta:
        model = GroupMessage
        fields = '__all__'
        

class ChatRoomListSerializer(serializers.ModelSerializer):

    is_full = serializers.BooleanField(read_only=True)
    latest_message = GroupMessageSerializer(source='group_messages.latest', read_only=True)

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
        latest_messages = obj.group_messages.order_by('-timestamp')[:30][::-1]
        
        # Serialize the messages using the GroupMessageSerializer
        serializer = GroupMessageSerializer(latest_messages, many=True)
        
        return serializer.data
    

class DirectMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()

    class Meta:
        model = DirectMessage
        fields = '__all__'
