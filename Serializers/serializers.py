from rest_framework import serializers
from rest_framework.serializers import Serializer
from transliterate import translit

from catalogs.models import Main_Categories
from Serializers.Exceptions import APIException202


def is_exist_category(value):
    if Main_Categories.objects.filter(name=value).exists():
        raise APIException202({'response': {'code': '0', 'errors': 'already exists'}})


def is_exist_subcategory(value):
    if Main_Categories.objects.filter(name=value['name'], category__name=value['category']).exists():
        raise APIException202({'response': {'code': '0', 'errors': 'already exists'}})


def validator_main(value):
    if not Main_Categories.objects.filter(main_categories=None).exists():
        raise APIException202({'response': {'code': '4', 'errors': 'anything not found'}})


def validator_sub(value):
    if not Main_Categories.objects.filter(main_categories=not None).exists():
        raise APIException202({'response': {'code': '4', 'errors': 'anything not found'}})


class Category_Serializer(Serializer):
    name = serializers.CharField(validators=[is_exist_category])

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], 'ru', reversed=True).replace("'", '').replace(" ",
                                                                                                                '_').lower()
        return Main_Categories.objects.create(**validated_data)


class Sub_Category_Serializer(Serializer):
    name = serializers.CharField()
    category = serializers.SlugField()

    def create(self, validated_data):
        validated_data['category'] = Main_Categories.objects.filter(slug=validated_data['category']).first()
        validated_data['slug'] = translit(validated_data['name'], 'ru', reversed=True).replace("'", '').replace(" ",
                                                                                                                '_').lower()
        is_exist_subcategory(validated_data)
        return Main_Categories.objects.create(**validated_data)


class Get_Category_Serializer(Serializer):
    object = serializers.ListField(validators=[validator_main], )
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        validated_data['code'] = '2'
        return {'response': validated_data}


class Get_SubCategory_Serializer(Serializer):
    object = serializers.ListField(validators=[validator_sub])
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        validated_data['code'] = '2'
        return {'response': validated_data}


class Products_Serializer(Serializer):
    pass