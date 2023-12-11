# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from chat.entity.models import ChatRoom, GroupMembership
from chat.service.permissions.chat_view_permissions import IsGroupMemberPermisssion
from . import serializers



class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = serializers.ChatRoomListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.my_groups.all()

    def perform_create(self, serializer):
        # Create the chat room
        chat_room = serializer.save()
        user = self.request.user

        GroupMembership.objects.create(room=chat_room, member=user, 
                        user_perm=GroupMembership.UserPermChoice.ADMIN)


class ChatRoomDetailView(generics.RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = serializers.ChatRoomDetailSerializer
    permission_classes = [IsGroupMemberPermisssion]


class LeaveChatRoomView(generics.UpdateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = serializers.ChatRoomDetailSerializer
    permission_classes = [IsGroupMemberPermisssion]

    def patch(self, request, *args, **kwargs):
        chatroom = self.get_object()
        user = self.request.user
        membership = GroupMembership.objects.get(room_id = chatroom.id, member_id = user.id)
        membership.delete()
        return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)


class EnterChatRoomView(generics.UpdateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = serializers.ChatRoomDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        chatroom = self.get_object()
        user = self.request.user
        validity, error_msg = chatroom.user_is_valid_in(user.id)
        if validity:
            GroupMembership.objects.create(room=chatroom, member=user)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

class ListMessagesView(generics.ListAPIView):
    serializer_class = serializers.GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        chat_room = get_object_or_404(ChatRoom, id = self.kwargs['chat_room_id'])
        return chat_room.group_messages.all().order_by('-timestamp')