from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.serializers import Serializer, ModelSerializer

from catalogs.models import Product, Features
from catalogs.models import Category
from extras.Exceptions import APIException202
from extras.slugifer import slugify


def is_exist_catalog(value: str) -> bool:
    if Category.objects.filter(name=value, category=None).exists():
        raise APIException202({'error': 'already exists'})
    return False


def is_exist_category(value: dict) -> bool:
    if Category.objects.filter(name=value['name'], category=value['category']).exists():
        raise APIException202({'error': 'already exists'})
    return False


class CatalogSerializer(ModelSerializer):
    name = serializers.CharField(validators=[is_exist_catalog],
                                 max_length=127,
                                 min_length=1)

    class Meta:
        model = Category
        fields = ['name', 'slug']

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data['name'])
        return Category.objects.create(**validated_data)


class CategorySerializer(CatalogSerializer):
    class Meta:
        model = Category
        fields = ["name", "category", "slug"]

    def validate(self, attrs):
        if not attrs.get("category"):
            raise NotFound()

        is_exist_category(attrs)
        return attrs


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
