#  Copyright (c) 2023. Kasimov Alexander, Ulyanovsk. All right reserved.

from rest_framework.viewsets import ModelViewSet

from apps.organizations.models import Organization
from apps.organizations.serializers import OrganizationSerializer
from core.permissions.permissions import IsManager, IsContributor, IsMaintainer, ReadOnly


class OrganizationViewSet(ModelViewSet):
    lookup_field = "slug"
    permission_classes = [ReadOnly | IsContributor | IsMaintainer | IsManager]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
