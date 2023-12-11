from rest_framework import permissions

class IsGroupMemberPermisssion(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users who are members of the room.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, room_obj):
        return room_obj.user_in_room(request.user.id)