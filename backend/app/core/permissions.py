from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from catalogs.models import Organization

CONTRIBUTOR_METHODS = ["put", "patch", "post"]


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsMaintainer(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        organization = Organization.objects.filter(maintainer=request.user)
        return organization.exists() | request.user.is_staff


class IsContributor(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        organization = Organization.objects.filter(contributors=request.user.id)
        return (organization.exists() & (request.method in CONTRIBUTOR_METHODS)) | request.user.is_staff
