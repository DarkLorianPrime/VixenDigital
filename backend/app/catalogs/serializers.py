from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.serializers import ModelSerializer

from catalogs.models import Category, Organization

from extras.slugifer import slugify


def is_exist_category(value: str, category=None) -> bool:
    if Category.objects.filter(name=value, category=category).exists():
        raise ValidationError({"category": 'already exists'}, code=409)

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

    def validate(self, attrs):
        if attrs["logo"].content_type not in ["image/jpeg", "image/png","image/tiff"]:
            raise ValidationError(detail={"logo": "the logo must be a picture"})

        return attrs

    def create(self, validated_data: dict):
        contributors = validated_data.pop("contributors", [])

        validated_data.update({"maintainer": self.context["request"].user,
                               "slug": slugify(validated_data['name'])})

        organization = Organization.objects.create(**validated_data)
        
        for contributor in contributors:
            organization.contributors.add(contributor)

        return organization
