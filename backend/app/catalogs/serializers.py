from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from backend.app.catalogs.models import Product, Features  # FeaturesForProduct
from backend.app.catalogs.models import Class as Category
from backend.app.extras.Exceptions import APIException202
from backend.app.extras.Serialize_Extra import translit


def is_exist_category(value):
    if Category.objects.filter(name=value, category=None).exists():
        raise APIException202({'errors': 'already exists'})


def is_exist_subcategory(value):
    if Category.objects.filter(name=value['name'], category=value['category']).exists():
        raise APIException202({'errors': 'already exists'})


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'category', 'slug']

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
        if validated_data.get('category') is None:
            is_exist_category(validated_data['name'])
            return Category.objects.create(**validated_data)
        is_exist_subcategory(validated_data)
        return Category.objects.create(**validated_data)


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'description', 'name', 'price', 'stock']

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], slugify=True, lower=True)
        return Product.objects.create(**validated_data)


# class Features_for_productSerializer(ModelSerializer):
#     class Meta:
#         model = FeaturesForProduct
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return FeaturesForProduct.objects.create(**validated_data)


class FeaturesSerializer(Serializer):
    name = serializers.CharField()
    slug = serializers.SlugField()
    catalog = serializers.SlugField()
    category = serializers.SlugField()
    required = serializers.BooleanField()

    def create(self, validated_data):
        category = Category.objects.get(slug=validated_data['category'],
                                        category__slug=validated_data['catalog'],
                                        category__category=None)
        validated_data['category'] = category
        return Features.objects.create(**validated_data)
