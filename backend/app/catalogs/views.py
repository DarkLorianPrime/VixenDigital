from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from catalogs.models import Organization
from catalogs.serializers import CatalogSerializer, CategorySerializer, OrganizationSerializer
from catalogs.service import Service
from core.permissions import ReadOnly

service = Service()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser | ReadOnly]

    def create(self, request, *args, **kwargs):
        values = request.data.dict()

        catalog = service.get_catalog(slug=kwargs["catalog"])

        if not catalog:
            raise NotFound()

        values["category"] = catalog.id

        serializer = self.get_serializer(data=values)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CatalogViewSet(ModelViewSet):
    serializer_class = CatalogSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser | ReadOnly]

    def get_queryset(self):
        return service.get_all_catalogs()


class OrganizationViewSet(ModelViewSet):
    lookup_field = "slug"
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = super().get_object()
        if (instance.maintainer == request.user) | request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise PermissionDenied()

# class SearchViewset(ViewSet):
#     def get(self, request, catalog, category):
#         get_data = self.request.GET
#
#         instance = Category.objects.filter(slug=category, category__slug=catalog, category__category=None).first()
#
#         if instance is None:
#             raise NotFound()
#
#         finally_get = Product.objects.filter(features__contains=get_data, category=category)
#
#         return Response(finally_get.values('name', 'slug'))
