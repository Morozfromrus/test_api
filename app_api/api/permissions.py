from rest_framework.permissions import DjangoModelPermissions, BasePermission

from app_api.apps import AppApiConfig


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['OPTIONS'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']

    def has_permission(self, request, view):
        if (
            getattr(view, '_ignore_model_permissions', False) or
            # crutch to force get_serializer_class working in extra actions
            request.user.has_perm('{}.{}'.format(AppApiConfig.name, view.action))
        ):
            return True

        return super().has_permission(request, view)


class OwnerPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or not hasattr(obj, 'is_owner'):
            return True

        return obj.is_owner(request.user)
