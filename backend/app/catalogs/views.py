from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
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

    def destroy(self, request, *args, **kwargs):
        instance = super().get_object()
        if instance.maintainer == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise PermissionDenied()
#
# class FeaturesViewSet(ViewSet):
#     def list(self, request, catalog, category):
#         """
#         Description:
#         For a construction of the type: URL/core/category/features/
#         For example: darklorian.space/Computers/Processors/features/
#         Get all features specified in specified products
#         ------
#         Request action: GET
#         ------
#         :param:  core : slug:
#             core in which there may be a category ↓
#         :param: category : slug:
#             category, in which we are looking for a product
#         :return: List of features of the specified products
#         """
#         instance = service.get_category(name=category, catalog=catalog)
#
#         if instance is None:
#             raise NotFound()
#
#         all_features = Features.objects.filter(category=instance)
#         # NEED_SERIALIZER
#         return Response(all_features.values('id', 'name', 'slug', 'required'))
#
#     def create(self, request, catalog, category):
#         """
#         Description:
#         Creates a new product in this category
#         ------
#         Request Action: POST
#         ------
#         Raises:
#         :raise An exception will be thrown if one of the parameters was not passed
#         -----
#         POST data (Parameters):
#         :param: name : str
#             Name of creating product.
#         :param: required : bool
#         :return:
#             Response with name of created feature
#         """
#         request_data = request.POST.dict()
#         request_data.update({"category": category, "catalog": catalog})
#
#         serialized = FeaturesSerializer(data=request_data)
#         serialized.is_valid(raise_exception=True)
#         serialized.save()
#
#         return Response(serialized.data, status=HTTP_201_CREATED)
#
#
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
