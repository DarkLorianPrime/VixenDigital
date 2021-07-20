from django.shortcuts import get_object_or_404, _get_queryset
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from catalogs.Exceptions import BadRequest, APIException202
from catalogs.models import Main_Categories, Product, Features
from catalogs.serializers import CategorySerializer, ProductsSerializer, GETProductsSerializer, GETFeaturesSerializer, \
    FeaturesSerializer
from extras.serialize_extra import translit
from extras.token_checker import token_checker


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    model = Main_Categories

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            return Main_Categories.objects.filter(category=None)
        returned = Main_Categories.objects.filter(slug=pk).first()
        if returned is None:
            raise APIException202(['Category Not Found'])
        return returned

    def retrieve(self, request, *args, **kwargs):
        returned = Main_Categories.objects.filter(category=self.get_queryset()).values('name')
        if not returned:
            return Response(['Not found products in this category'])
        return Response(returned)

    def post(self, request, *args, **kwargs):
        parameters = request.POST.dict()
        returned = self.get_serializer(data={'name': parameters.get('name'), 'category': self.get_queryset().id})
        returned.is_valid(True)
        returned.save()
        return Response(returned.validated_data['name'])


class Products(ViewSet):
    def list(self, request, mainCategory, subCategory):
        category = Main_Categories.objects.filter(slug=subCategory).first()
        all_categories = Product.objects.filter(category=category)
        data = {'object': all_categories.values(), 'count': all_categories.count()}
        serializer = GETProductsSerializer(data=data)
        serializer.is_valid(True)
        return Response(serializer.validated_data)

    @token_checker
    def create(self, request, mainCategory, subCategory):
        new_data_for_serializer = request.GET.dict()
        new_data_for_serializer['features'] = Features.objects.filter(
            name__in=request.GET.get('features').split(', ')).values_list('id', flat=True)
        new_data_for_serializer['slug'] = translit(new_data_for_serializer['name'], slugify=True, lower=True)
        new_data_for_serializer['category'] = Main_Categories.objects.filter(slug=subCategory).first().id
        if not new_data_for_serializer['features']:
            raise BadRequest({"features": ["Этих особенностей нет в данной категории."]})
        products = ProductsSerializer(data=new_data_for_serializer)
        products.is_valid(True)
        products.save()
        return Response({"features": [products.validated_data['name']]})


class FeaturesViewSet(ViewSet):
    def list(self, request, mainCategory, subCategory):
        category = Main_Categories.objects.filter(slug=subCategory).first()
        all_features = Features.objects.filter(category=category)
        features_template = {'object': all_features.values(), 'count': all_features.count()}
        features = GETFeaturesSerializer(data=features_template)
        features.is_valid(True)
        return Response(features.validated_data)

    def create(self, request, mainCategory, subCategory):
        request_data = request.GET.dict()
        request_data['category'] = subCategory
        serialized = FeaturesSerializer(data=request_data)
        serialized.is_valid(True)
        serialized.save()
        return Response({"features": [serialized.validated_data]})
# 13a_6gQ3ABi9GrZT59yMLw
