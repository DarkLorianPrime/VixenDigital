from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS

from core.permissions.service import Service

CONTRIBUTOR_METHODS = ["put", "patch", "post"]
service = Service()


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            token = request.headers.get("X-ADMIN-TOKEN")
            if not token or not token.isdigit():
                raise PermissionDenied("X-ADMIN-TOKEN is invalid or not passed")

            is_valid = service.is_valid_user_admin_password(user=request.user, admin_password=token)

            if not is_valid:
                raise PermissionDenied("X-ADMIN-TOKEN is invalid")

            return True

        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsMaintainer(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        organization = service.is_organization_exists(maintainer=request.user)
        return organization | request.user.is_staff


class IsContributor(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        organization = service.is_organization_exists(contributors=request.user)
        return (organization and (request.method in CONTRIBUTOR_METHODS)) or request.user.is_staff
