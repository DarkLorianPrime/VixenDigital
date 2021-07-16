from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from Serializers.Exceptions import APIException202
from catalogs.models import Main_Categories
from extras.codes_list import codelist
from extras.token_checker import token_checker
from Serializers.serializers import Category_Serializer, Sub_Category_Serializer, Get_Category_Serializer, \
    Get_SubCategory_Serializer


class First_Page(ViewSet):
    def list(self, request):
        Category_force = Main_Categories.objects.filter(category=None)
        data = {'object': Category_force.values('slug', 'name'), 'count': Category_force.count()}
        serialize_data = Get_Category_Serializer(data=data)
        serialize_data.validate(data)
        #raise APIException202({'response': {'code': '6', 'errors': serialize_data.errors}})
        return Response(serialize_data.validated_data)

    @token_checker
    def create(self, request):
        serialized = Category_Serializer(data=request.GET.dict())
        serialized.is_valid(True)
        # if not serialized.is_valid():
        #     raise APIException202({'response': {'code': '6', 'errors': serialized.errors}})
        comm = serialized.save()
        return Response({'response': {'code': '1', 'object': f'{comm}'}})


class Get_Codes(ViewSet):
    def list(self, request):
        return Response({'response': codelist(), 'code': '2'})


class Sub_Category(ViewSet):
    def list(self, request, mainCategory):
        all_categories = Main_Categories.objects.filter(category=Main_Categories.objects.filter(slug=mainCategory).first())
        data = {'object': all_categories.values('slug', 'name'), 'count': all_categories.count()}
        serialized = Get_SubCategory_Serializer(data)
        if not serialized.is_valid():
            raise APIException202({'response': {'code': '6', 'errors': serialized.errors}})
        return Response(serialized)

    @token_checker
    def create(self, request, mainCategory):
        request_data = request.GET.dict()
        request_data['category'] = mainCategory
        serialized = Sub_Category_Serializer(data=request_data)
        if not serialized.is_valid():
            return Response({'response': {'code': '6', 'errors': serialized.errors}})
        returned = serialized.save()
        return Response({'response': {'code': '1', 'object': returned.name}})


class Products(ViewSet):
    def get(self, request, mainCategory, subCategory):
        all_categories = Main_Categories.objects.filter(slug=subCategory,
                                                        category=Main_Categories.objects.filter(
                                                            slug=mainCategory).first())
        if not all_categories.exists():
            return Response({'response': {'code': '4', 'errors': 'anything not found'}})
        return Response({'lox': 'chmo'})

# 13a_6gQ3ABi9GrZT59yMLw
