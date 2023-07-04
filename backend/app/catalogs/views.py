from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet, ModelViewSet

from catalogs.models import Product, Features
from catalogs.models import Category
from catalogs.serializers import CatalogSerializer, ProductsSerializer, FeaturesSerializer, CategorySerializer
from core.permissions import ReadOnly


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = "slug"
    allowed_endpoints = ["GET", "HEAD"]
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_queryset(self):
        catalog = self.kwargs.get("catalog")
        if not catalog:
            raise NotFound()

        return Category.objects.filter(category__slug=catalog)

    def create(self, request, *args, **kwargs):
        values = request.data.dict()

        catalog = Category.objects.filter(slug=kwargs["catalog"]).first()

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

    def get_queryset(self):
        return Category.objects.filter(category=None)


class Products(ViewSet):
    def list(self, request, catalog, category):
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
        category_instance: Category = Category.objects.filter(slug=category,
                                                              category__slug=catalog,
                                                              category__category=None).first()

        if category_instance is None:
            raise NotFound(f"Категория {catalog}/{category} не найдена")

        products = Product.objects.filter(category=category_instance)

        # NEED_SERIALIZER
        return Response(products.values())

    def create(self, request, catalog, category):
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
        exclude_list = ['name', 'description', 'price', 'stock', 'category']
        features_json = {}
        product_information = request.POST.dict()
        category = Category.objects.get(slug=category,
                                        category__slug=catalog,
                                        category__category=None)

        if not category.exists():
            return Response({['Category not found']})

        product_information['category'] = category.id
        new_product = ProductsSerializer(data=product_information)
        new_product.is_valid(raise_exception=True)
        required_features = list(
            Features.objects.filter(category=category, required=True).values_list('slug', flat=True))

        for features_name, value_name in product_information.items():
            if features_name in exclude_list:
                continue
            if features_name in required_features:
                required_features.remove(features_name)
            features_json[features_name] = value_name

        if len(required_features) > 0:
            return Response({'error': 'Ты не указал обязательные features (slug):', 'arguments': required_features})
        new_product.features = features_json
        new_product.save()

        # NEED_SERIALIZER !!!!
        return Response([{'name': new_product.validated_data["name"], 'features': features_json}])


class FeaturesViewSet(ViewSet):
    def list(self, request, catalog, category):
        """
        Description:
        For a construction of the type: URL/core/category/features/
        For example: darklorian.space/Computers/Processors/features/
        Get all features specified in specified products
        ------
        Request action: GET
        ------
        :param:  core : slug:
            core in which there may be a category ↓
        :param: category : slug:
            category, in which we are looking for a product
        :return: List of features of the specified products
        """
        instance = Category.objects.filter(slug=category, category__slug=catalog, category__category=None).first()

        if instance is None:
            raise NotFound()

        all_features = Features.objects.filter(category=instance)
        # NEED_SERIALIZER
        return Response(all_features.values('id', 'name', 'slug', 'required'))

    def create(self, request, catalog, category):
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
        :param: required : bool
        :return:
            Response with name of created feature
        """
        request_data = request.POST.dict()
        request_data.update({"category": category, "catalog": catalog})

        serialized = FeaturesSerializer(data=request_data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status=HTTP_201_CREATED)


class SearchViewset(ViewSet):
    def get(self, request, catalog, category):
        get_data = self.request.GET

        instance = Category.objects.filter(slug=category, category__slug=catalog, category__category=None).first()

        if instance is None:
            raise NotFound()

        finally_get = Product.objects.filter(features__contains=get_data, category=category)

        return Response(finally_get.values('name', 'slug'))
