#  Copyright (c) 2023. Kasimov Alexander, Ulyanovsk. All right reserved.

from rest_framework.routers import SimpleRouter

from apps.organizations.views import OrganizationViewSet

organization_router = SimpleRouter()
organization_router.register(r"", OrganizationViewSet, basename="Organization")

urlpatterns = organization_router.urls
