from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.serializers import Serializer, ModelSerializer

from catalogs.models import Category, Organization

from extras.slugifer import slugify


def is_exist_category(value: str, category=None) -> bool:
    if Category.objects.filter(name=value, category=category).exists():
        raise ValidationError('already exists', code=409)
    return False


def is_exist_organization(name: str) -> bool:
    if Organization.objects.filter(name=name).exists():
        raise ValidationError('already exists', code=409)
    return False


class CatalogSerializer(ModelSerializer):
    name = serializers.CharField(validators=[is_exist_category], max_length=127, min_length=1)

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

        is_exist_category(attrs["name"], attrs["category"])
        return attrs


class OrganizationSerializer(ModelSerializer):
    name = serializers.CharField(validators=[is_exist_organization])

    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        if not validated_data["contributors"]:
            validated_data.pop("contributors")
        validated_data["slug"] = slugify(validated_data['name'])
        return Organization.objects.create(**validated_data)


# class FeaturesSerializer(Serializer):
#     name = serializers.CharField()
#     slug = serializers.SlugField()
#     catalog = serializers.SlugField()
#     category = serializers.SlugField()
#     required = serializers.BooleanField()
#
#     def create(self, validated_data):
#         category = Category.objects.get(slug=validated_data['category'],
#                                         category__slug=validated_data['catalog'],
#                                         category__category=None)
#         validated_data['category'] = category
#         return Features.objects.create(**validated_data)
