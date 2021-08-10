from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from catalogs.models import Main_Categories, Product, Features, Features_for_product
from extras.Exceptions import APIException202
from extras.serialize_extra import translit


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


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'description', 'name', 'price', 'stock']

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
        return Product.objects.create(**validated_data)


class Features_for_productSerializer(ModelSerializer):
    class Meta:
        model = Features_for_product
        fields = '__all__'

    def create(self, validated_data):
        return Features_for_product.objects.create(**validated_data)


class FeaturesSerializer(Serializer):
    name = serializers.CharField()
    catalog = serializers.SlugField()
    category = serializers.SlugField()
    required = serializers.BooleanField()

    def create(self, validated_data):
        main_category = Main_Categories.objects.get(slug=validated_data['catalog'], category=None)
        data = Main_Categories.objects.get(slug=validated_data['category'], category=main_category)
        validated_data['category'] = data
        return Features.objects.create(**{'name': validated_data['name'], 'category': validated_data['category'], 'required': validated_data['required']})

