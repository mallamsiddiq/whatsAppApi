
from django.contrib.auth.mixins import LoginRequiredMixin


class GroupMemberRequiredMixin(LoginRequiredMixin):
    """
    Mixin that ensures only members of the chat room can access the view.
    """
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if the user is a member of the chat room
        chat_room = self.get_object()
        user = self.request.user

        if not chat_room.user_in_room(user.id):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
