from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from chat.entity.models import ChatRoom, GroupMembership, Conversation
from chat.service.permissions.chat_view_permissions import IsGroupMemberPermisssion
from . import serializers

class ChatRoomViewSet(viewsets.generivieset, retrivemodemixin, listmdmixin):
    serializer_class = serializers.ChatRoomDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(members=user)

    def perform_create(self, serializer):
        chat_room = serializer.save()
        user = self.request.user
        GroupMembership.objects.create(room=chat_room, member=user, user_perm=GroupMembership.UserPermChoice.ADMIN)

    def get_permissions(self):

        if self.action in ['update', 'destroy']:
            return [permissions.IsAdminUser]
        return [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enter_room(self, request, pk=None):
        chat_room = self.get_object()
        user = request.user
        
        validity, error_msg = chat_room.user_is_valid_in(user.id)
        if validity:
            GroupMembership.objects.create(room=chat_room, member=user)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsGroupMemberPermisssion])
    def leave_room(self, request, pk=None):
        chat_room = self.get_object()
        user = request.user

        membership = GroupMembership.objects.filter(room=chat_room, member=user).first()
        if membership:
            membership.delete()
            return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You are not a member of this chat room.'}, status=status.HTTP_400_BAD_REQUEST)


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Assuming the Conversation model has a ManyToManyField or similar for users
        return Conversation.objects.filter(members=user)


class ListMessagesView(generics.ListAPIView):
    serializer_class = serializers.GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        chat_room = get_object_or_404(ChatRoom, id = self.kwargs['chat_room_id'])
        return chat_room.group_messages.all().order_by('-timestamp')
    
