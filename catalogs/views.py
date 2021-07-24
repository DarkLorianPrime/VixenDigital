from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from catalogs.Exceptions import APIException202
from catalogs.models import Main_Categories, Product, Features
from catalogs.serializers import CategorySerializer, ProductsSerializer, FeaturesSerializer


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    model = Main_Categories

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            returned = Main_Categories.objects.filter(category=None)
            if not returned:
                raise APIException202([{'Category Not Found'}])
            return returned
        returned = Main_Categories.objects.filter(slug=pk).first()
        if returned is None:
            raise APIException202([{'Category Not Found'}])
        return returned

    def retrieve(self, request, *args, **kwargs):
        returned = Main_Categories.objects.filter(category=self.get_queryset()).values('name')
        if not returned:
            return Response([{'Not found products in this category'}])
        return Response(returned)

    def post(self, request, *args, **kwargs):
        parameters = request.POST.dict()
        returned = self.get_serializer(data={'name': parameters.get('name'), 'category': self.get_queryset().id})
        returned.is_valid(True)
        returned.save()
        return Response([{'name': returned.validated_data['name']}])


class Products(ViewSet):
    def list(self, request, globalcategory, category):
        main_category = Main_Categories.objects.get(slug=globalcategory)
        give_category = Main_Categories.objects.get(slug=category, category=main_category)
        products = Product.objects.filter(category=give_category).values()
        return Response([{products}])

    def create(self, request, globalcategory, category):
        product_information = request.POST.dict()
        main_category = Main_Categories.objects.get(slug=globalcategory)
        product_information['category'] = Main_Categories.objects.get(slug=category, category=main_category).id
        features = product_information.get('features')
        features_get = features.split(', ') if features is not None else []
        features_list = Features.objects.filter(name__in=features_get).values_list('id', flat=True)
        new_product = ProductsSerializer(data=product_information)
        new_product.is_valid(True)
        new_product.save()
        for one_features in features_list:
            new_product.instance.features.add(one_features)
        return Response({'name': [new_product.validated_data['name']]})


class FeaturesViewSet(ViewSet):
    def list(self, request, mainCategory, subCategory):
        main_category = Main_Categories.objects.get(slug=mainCategory)
        category = Main_Categories.objects.get(slug=subCategory, category=main_category)
        all_features = Features.objects.filter(category=category)
        return Response(all_features.values('name'))

    def create(self, request, mainCategory, subCategory):
        request_data = request.POST.dict()
        request_data['category'] = subCategory
        serialized = FeaturesSerializer(data=request_data)
        serialized.is_valid(True)
        serialized.save()
        return Response({"name": [serialized.validated_data['name']]})


# unused token 13a_6gQ3ABi9GrZT59yMLw
