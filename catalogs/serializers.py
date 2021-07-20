from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from catalogs.models import Main_Categories, Product, Features, Access_Token
from catalogs.Exceptions import APIException202
from extras.serialize_extra import translit
from extras.token_checker import token_checker


# def is_valid_token(token):
#     if token is None:
#         raise APIException202({'errors': 'access_token not found'})
#     if not Access_Token.objects.filter(token=token['name']).exists():
#         raise APIException202({'errors': 'access_token not valid'})


def is_exist_category(value):
    if Main_Categories.objects.filter(name=value, category=None).exists():
        raise APIException202({'errors': 'already exists'})


def is_exist_subcategory(value):
    if Main_Categories.objects.filter(name=value['name'], category=value['category']).exists():
        raise APIException202({'errors': 'already exists'})


def validator_main(value):
    if not Main_Categories.objects.filter(main_categories=None).exists():
        raise APIException202({'errors': 'anything not found'})


def validator_sub(value):
    if not Main_Categories.objects.filter(main_categories=not None).exists():
        raise APIException202({'errors': 'anything not found'})


#class CategorySerializer(Serializer):
#    name = serializers.CharField(validators=[is_exist_category])
#
#    def create(self, validated_data):
#        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
#        return Main_Categories.objects.create(**validated_data)

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Main_Categories
        fields = ['name', 'category']

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
        if validated_data.get('category') is None:
            is_exist_category(validated_data['name'])
            return Main_Categories.objects.create(**validated_data)
        is_exist_subcategory(validated_data)
        return Main_Categories.objects.create(**validated_data)


class GETSubCategorySerializer(Serializer):
    class Meta:
        model = Main_Categories
        fields = ['name', 'category']

    def create(self, validated_data):
        print(validated_data)
        return validated_data


class GETProductsSerializer(Serializer):
    object = serializers.ListField()
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        return validated_data


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class GETFeaturesSerializer(Serializer):
    object = serializers.ListField()
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        return validated_data


class FeaturesSerializer(Serializer):
    name = serializers.CharField()
    category = serializers.SlugField()

    def create(self, validated_data):
        data = Main_Categories.objects.filter(slug=validated_data['category']).first()
        validated_data['category'] = data
        return Features.objects.create(**validated_data)

# class Products_Serializer(Serializer):
#    category = serializers.CharField()
#    feauters = serializers.ListField()
#    description = serializers.CharField()
#    name = serializers.CharField()
#    slug = serializers.CharField()
#    price = serializers.IntegerField()
