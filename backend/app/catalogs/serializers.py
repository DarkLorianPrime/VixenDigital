from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from catalogs.models import Product, Features
from catalogs.models import Class as Category
from extras.Exceptions import APIException202
from extras.slugifer import slugify

WO = {"write_only": True}


def is_exist_catalog(value: str) -> bool:
    if Category.objects.filter(name=value, category=None).exists():
        raise APIException202({'error': 'already exists'})
    return False


def is_exist_category(value: dict) -> bool:
    if Category.objects.filter(name=value['name'], category=value['category']).exists():
        raise APIException202({'error': 'already exists'})
    return False


class CategorySerializer(ModelSerializer):
    name = serializers.CharField(validators=[is_exist_catalog])

    def validate(self, attrs):
        if attrs.get("category"):
            is_exist_category(attrs)
        return attrs

    class Meta:
        model = Category
        fields = ['name', 'category', 'slug']

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data['name'])
        return Category.objects.create(**validated_data)


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'description', 'name', 'price', 'stock']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return Product.objects.create(**validated_data)


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
