from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet, ModelViewSet

from catalogs.models import Category
from core.permissions import ReadOnly
from products.models import Product
from products.serializers import ProductsSerializer, FeatureSerializer
from products.service import Service

product = Product()
service = Service()


class ProductsViewSet(ViewSet):
    serializer_class = ProductsSerializer

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
        category_instance: Category = service.get_category(**self.kwargs)

        if category_instance is None:
            raise NotFound()

        products = product.objects.filter(category=category_instance.id).parse()
        # NEED_SERIALIZER
        return Response(products[0]["hits"])

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
        category = service.get_category(**self.kwargs)
        if category is None:
            raise NotFound()

        values = request.POST.dict()
        values.update({"owner_id": request.user.id,
                       "category_id": category.id})

        features_params = service.get_user_features(values)
        required_params = service.get_required_features(category_id=category.id)
        print(required_params, features_params)
        # filter(lambda x: ..., required_params)
        serializer = self.serializer_class(data=values)
        serializer.is_valid(raise_exception=True)

        exclude_list = ['name', 'description', 'price', 'stock', 'category']
        features_json = {}
        product_information = request.POST.dict()

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

        if required_features:
            return Response({'error': 'Ты не указал обязательные features (slug):', 'arguments': required_features})

        new_product.features = features_json
        new_product.save()

        # NEED_SERIALIZER !! !!
        return Response([{'name': new_product.validated_data["name"], 'features': features_json}])


class FeaturesViewSet(ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = FeatureSerializer
    lookup_field = "name"

    def get_object(self):
        category_id = self.request.category.id
        feature = service.get_feature(category_id, **{self.lookup_field: self.kwargs["name"]})

        if not feature:
            raise NotFound()

        return feature

    def list(self, request, *args, **kwargs):
        features = service.get_all_features(category_id=request.category.id)
        serializer = self.serializer_class(features, many=True)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def perform_destroy(self, instance):
        service.delete_feature(instance)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"category_id": self.request.category.id})
        return context
