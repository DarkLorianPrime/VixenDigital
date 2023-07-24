from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.catalogs.models import Category, Organization
from apps.catalogs.repositories import CategoryRepository, OrganizationRepository

from core.slugifer import slugify

categories_repo = CategoryRepository()
organizations_repo = OrganizationRepository()


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


class OrganizationSerializer(ModelSerializer):
    name = serializers.CharField()
    maintainer = serializers.CharField(default=None)
    contributors = serializers.ListField(write_only=True)
    logo = serializers.ImageField()
    slug = serializers.SlugField(default=None)
    verified = serializers.BooleanField(default=False)

    class Meta:
        model = Organization
        fields = "__all__"

    @property
    def method(self):
        return self.context["request"].method

    def validate_verified(self, verified):
        if self.context["request"].user.is_staff:
            return verified

        return False

    def validate_logo(self, image):
        if self.method in ["PUT", "PATCH"]:
            organizations_repo.organization_logo_delete(instance=self.instance)

        return image

    def validate_name(self, name):
        self.context["name"] = name

        instance: Organization | dict = self.instance or {}
        instance_name = getattr(instance, "name", None)

        if instance_name == name:
            return name

        return organizations_repo.is_exist_organization(name=name)

    def validate_maintainer(self, _):
        user = self.context["request"].user
        if self.method == "POST":
            return user

        return organizations_repo.get_maintainer(user)

    def validate_slug(self, _):
        return slugify(self.context["name"])

    def validate_contributors(self, contributors):
        return organizations_repo.get_contributors(contributors)
