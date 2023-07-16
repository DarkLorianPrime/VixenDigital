from collections import ChainMap

from django.db.models import Q
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from catalogs.repositories import OrganizationRepository
from core.permissions import ReadOnly, IsMaintainer, IsContributor
from products.serializers import FullInfoProductSerializer, FeatureSerializer, SmallInfoProductSerializer
from products.repositories import ProductRepository, FeatureRepository

products_repo = ProductRepository()
features_repo = FeatureRepository()
organization_repo = OrganizationRepository()


class ProductsViewSet(ModelViewSet):
    lookup_field = "slug"
    permission_classes = [IsAdminUser | IsMaintainer | IsContributor | ReadOnly]

    def get_object(self):
        category_id = self.request.category.id
        feature = products_repo.get_product(category_id, **{self.lookup_field: self.kwargs["slug"]})

        if not feature:
            raise NotFound()

        user = self.request.user
        organization = organization_repo.get_organization(id=feature["owner"])
        is_personal = organization.maintainer == user or user in organization.contributors

        if feature["visible"] or is_personal or user.is_staff:
            return feature

        raise NotFound()

    def get_queryset(self):
        return products_repo.get_all_products(self.request.category.id, True)

    def get_serializer_class(self):
        if self.action == "list":
            return SmallInfoProductSerializer

        return FullInfoProductSerializer

    def perform_destroy(self, instance):
        products_repo.delete_product(instance)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"category_id": self.request.category.id})
        return context

    def list(self, request, *args, **kwargs):
        """
        Description:
        For a construction of the type: URL/core/category
        For example: darklorian.space/Computers/Processors
        Get all products specified in specified category
        ------
        Request action: GET
        ------
        :param:  core : slug:
            core in which there may be a category ↓
        :param: category : slug:
            category, in which we are looking for a product
        :return: List of products
        """
        products = products_repo.get_all_products(category_id=self.request.category.id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Description:
        Creates a new product in this category
        ------
        Request Action: POST
        ------
        Raises:
        :raise An exception will be thrown if one of the parameters was not passed
        -----
        POST data (Parameters):
        :param: name : str
            Name of creating product.
        :param: category : model.id
            An unspecified parameter.
        :param: (Many) features : many args
            Features from the features list.
        :param: description : str
            Information about this product
        :param: slug : slug
            An unspecified parameter.
        :param: price : int
            Price in rubles
        :param: stock : int
            quantity of goods in stock
        :return:
            Response with name of created product
        """
        values = request.POST.dict()
        category = self.request.category

        inserted_features = features_repo.get_user_features(values)
        all_features = features_repo.get_all_features(category_id=category.id)

        system_features = {full["name"]: full for full in all_features}
        keys_features = {full["name"] for full in all_features if full["required"]}

        keys_inserted = dict(ChainMap(*inserted_features))

        difference = features_repo.difference_features(keys_features, keys_inserted.keys())
        not_valid_values = features_repo.check_value_valid(system_features, keys_inserted)

        if difference[0] or not_valid_values:
            raise ValidationError({**difference[0], **not_valid_values}, code=400)

        params = [
            {
                "slug": key,
                "value": element,
                "display_name": system_features[key]["display_name"],
                "unit": system_features[key]["unit"]
            }
            for key, element in keys_inserted.items() if key in difference[1]]

        values["features"] = params

        serializer = self.get_serializer(data=values)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


class FeaturesViewSet(ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = FeatureSerializer
    lookup_field = "name"

    def get_object(self):
        category_id = self.request.category.id
        feature = features_repo.get_feature(category_id, **{self.lookup_field: self.kwargs["name"]})

        if not feature:
            raise NotFound()

        return feature

    def list(self, request, *args, **kwargs):
        features = features_repo.get_all_features(category_id=request.category.id)
        serializer = self.get_serializer(features, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        features_repo.delete_feature(instance)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"category_id": self.request.category.id})
        return context
