from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.catalogs.models import Organization
from apps.catalogs.serializers import CatalogSerializer, CategorySerializer, OrganizationSerializer
from apps.catalogs.repositories import CategoryRepository
from core.permissions.permissions import ReadOnly, IsMaintainer, IsContributor, IsManager

service = CategoryRepository()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [IsManager | ReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"category_id": self.request.category.id})
        return context

    def get_queryset(self):
        return self.request.category.categories

    def create(self, request, *args, **kwargs):
        values = request.data
        if values:
            values = values.dict()

        serializer = self.get_serializer(data=values)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CatalogViewSet(ModelViewSet):
    serializer_class = CatalogSerializer
    lookup_field = "slug"
    permission_classes = [IsManager | ReadOnly]

    def get_queryset(self):
        return service.get_all_catalogs()


class OrganizationViewSet(ModelViewSet):
    lookup_field = "slug"
    permission_classes = [IsManager | IsContributor | IsMaintainer | ReadOnly]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

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