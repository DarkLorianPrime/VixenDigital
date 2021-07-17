from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from transliterate import translit

from Serializers.Exceptions import BadRequest
from catalogs.models import Main_Categories, Product, Features
from extras.codes_list import codelist
from extras.token_checker import token_checker
from Serializers import Category_Serializer, Sub_Category_Serializer, Get_Category_Serializer, \
    Get_SubCategory_Serializer, Products_Serializer, Get_Products_Serializer, Get_Features_Serializer, \
    Features_Serializer


class First_Page(ViewSet):
    def list(self, request):
        Category_force = Main_Categories.objects.filter(category=None)
        data = {'object': Category_force.values('slug', 'name'), 'count': Category_force.count()}
        serialize_data = Get_Category_Serializer(data=data)
        serialize_data.is_valid(True)
        return Response(serialize_data.validated_data)

    @token_checker
    def create(self, request):
        serialized = Category_Serializer(data=request.GET.dict())
        serialized.is_valid(True)
        comm = serialized.save()
        return Response({'object': f'{comm}'})


class Get_Codes(ViewSet):
    def list(self, request):
        return Response({'response': codelist(), 'code': '2'})


class Sub_Category(ViewSet):
    def list(self, request, mainCategory):
        all_categories = Main_Categories.objects.filter(
            category=Main_Categories.objects.filter(slug=mainCategory).first())
        data = {'object': all_categories.values('slug', 'name'), 'count': all_categories.count()}
        serialized = Get_SubCategory_Serializer(data=data)
        serialized.is_valid(raise_exception=True)
        return Response(serialized.validated_data)

    @token_checker
    def create(self, request, mainCategory):
        request_data = request.GET.dict()
        request_data['category'] = mainCategory
        serialized = Sub_Category_Serializer(data=request_data)
        serialized.is_valid(True)
        returned = serialized.save()
        return Response({'response': {'code': '1', 'object': returned.name}})


class Products(ViewSet):
    def list(self, request, mainCategory, subCategory):
        category = Main_Categories.objects.filter(slug=subCategory).first()
        all_categories = Product.objects.filter(category=category)
        data = {'object': all_categories.values(), 'count': all_categories.count()}
        serializer = Get_Products_Serializer(data=data)
        serializer.is_valid(True)
        return Response(serializer.validated_data)

    @token_checker
    def create(self, request, mainCategory, subCategory):
        new_data_for_serializer = request.GET.dict()
        new_data_for_serializer['features'] = Features.objects.filter(
            name__in=request.GET.get('features').split(', ')).values_list('id', flat=True)
        new_data_for_serializer['slug'] = translit(new_data_for_serializer['name'], 'ru', reversed=True).replace(
            "'", '').replace(" ", '_').lower()
        new_data_for_serializer['category'] = Main_Categories.objects.filter(slug=subCategory).first().id
        if not new_data_for_serializer['features']:
            raise BadRequest({"features": ["Этих особенностей нет в данной категории."]})
        products = Products_Serializer(data=new_data_for_serializer)
        products.is_valid(True)
        products.save()
        return Response({"features": [products.validated_data['name']]})


class Features_ViewSet(ViewSet):
    def list(self, request, mainCategory, subCategory):
        category = Main_Categories.objects.filter(slug=subCategory).first()
        all_features = Features.objects.filter(category=category)
        features_template = {'object': all_features.values(), 'count': all_features.count()}
        features = Get_Features_Serializer(data=features_template)
        features.is_valid(True)
        return Response(features.validated_data)

    def create(self, request, mainCategory, subCategory):
        request_data = request.GET.dict()
        request_data['category'] = subCategory
        serialized = Features_Serializer(data=request_data)
        serialized.is_valid(True)
        serialized.save()
        return Response({"features": [serialized.validated_data]})
# 13a_6gQ3ABi9GrZT59yMLw
