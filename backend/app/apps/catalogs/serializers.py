from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.catalogs.models import Category
from apps.catalogs.repositories import CategoryRepository

from core.slugifer import slugify

categories_repo = CategoryRepository()


class CatalogSerializer(ModelSerializer):
    name = serializers.CharField(validators=[categories_repo.is_exist_category], max_length=127, min_length=8)

    class Meta:
        model = Category
        fields = ['name', 'slug']

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data['name'])
        return categories_repo.create_category(**validated_data)


class CategorySerializer(CatalogSerializer):
    category = serializers.SlugField(default=None)

    class Meta:
        model = Category
        fields = ["name", "category", "slug"]

    def validate_category(self, _):
        return self.context["category_id"]

    def validate(self, attrs):
        categories_repo.is_exist_category(attrs["name"], attrs["category"])
        return attrs