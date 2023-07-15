from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.serializers import ModelSerializer

from authorization.models import User
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
    name = serializers.CharField()
    maintainer = serializers.CharField(default=None)
    contributors = serializers.ListField(write_only=True)
    logo = serializers.ImageField()
    slug = serializers.SlugField(default=None)

    class Meta:
        model = Organization
        fields = "__all__"

    @property
    def method(self):
        return self.context["request"].method

    def validate_logo(self, image):
        if self.method in ["PUT", "PATCH"]:
            self.instance.logo.delete()

        return image

    def validate_name(self, name):
        self.context["name"] = name

        instance: Organization | dict = self.instance or {}
        instance_name = getattr(instance, "name", None)

        if instance_name == name:
            return name
        
        if instance_name is None:
            if Organization.objects.filter(name=name).exists():
                raise ValidationError('already exists', code=409)

        return name

    def validate_maintainer(self, _):
        user = self.context["request"].user
        if self.method == "POST":
            return user

        return Organization.objects.filter(Q(maintainer=user) | Q(contributors=user)).first().maintainer

    def validate_slug(self, _):
        return slugify(self.context["name"])

    def validate_contributors(self, contributors):
        return User.objects.filter(id__in=contributors).all()
