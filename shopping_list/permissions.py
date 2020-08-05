from xauth import permissions


class IsOwnerOrSuperuser(permissions.IsOwnerOrSuperuser):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(obj.owner == user.id or user.is_superuser)
