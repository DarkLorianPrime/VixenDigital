from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from catalogs.models import Categories, Product, Features, FeaturesForProduct
from extras.Exceptions import APIException202
from extras.serialize_extra import translit


def is_exist_category(value):
    if Categories.objects.filter(name=value, category=None).exists():
        raise APIException202({'errors': 'already exists'})


def is_exist_subcategory(value):
    if Categories.objects.filter(name=value['name'], category=value['category']).exists():
        raise APIException202({'errors': 'already exists'})


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ['name', 'category', 'slug']

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
        if validated_data.get('category') is None:
            is_exist_category(validated_data['name'])
            return Categories.objects.create(**validated_data)
        is_exist_subcategory(validated_data)
        return Categories.objects.create(**validated_data)


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'description', 'name', 'price', 'stock']

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
        return Product.objects.create(**validated_data)


class Features_for_productSerializer(ModelSerializer):
    class Meta:
        model = FeaturesForProduct
        fields = '__all__'

    def create(self, validated_data):
        return FeaturesForProduct.objects.create(**validated_data)


class FeaturesSerializer(Serializer):
    name = serializers.CharField()
    catalog = serializers.SlugField()
    category = serializers.SlugField()
    required = serializers.BooleanField()

    def create(self, validated_data):
        main_category = Categories.objects.get(slug=validated_data['catalog'], category=None)
        data = Categories.objects.get(slug=validated_data['category'], category=main_category)
        validated_data['category'] = data
        return Features.objects.create(**{'name': validated_data['name'], 'category': validated_data['category'], 'required': validated_data['required']})

